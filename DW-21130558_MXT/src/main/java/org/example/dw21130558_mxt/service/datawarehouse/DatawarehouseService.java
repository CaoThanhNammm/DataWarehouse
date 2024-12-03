package org.example.dw21130558_mxt.service.datawarehouse;


import jakarta.annotation.PostConstruct;
import org.example.dw21130558_mxt.model.control.Log;
import org.example.dw21130558_mxt.service.control.ControlLogService;
import org.example.dw21130558_mxt.service.control.EmailService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import org.springframework.scheduling.annotation.Scheduled;

@Service
public class DatawarehouseService {

    @Autowired
    private ControlLogService controlLogService;

    private EmailService emailService;
    private final JdbcTemplate dwJdbcTemplate;
    private final JdbcTemplate dmJdbcTemplate;

    private boolean isDataLoaded = false;

    @Autowired
    public DatawarehouseService(JdbcTemplate dwJdbcTemplate, JdbcTemplate dmJdbcTemplate) {
        this.dwJdbcTemplate = dwJdbcTemplate;
        this.dmJdbcTemplate = dmJdbcTemplate;
    }

    @PostConstruct
    public void init() {
        // Gọi phương thức load dữ liệu từ DW vào DM
        if (!isDataLoaded) {
            loadDataFromStagingToDW();
            isDataLoaded = true;  // Đánh dấu rằng dữ liệu đã được tải
        }
    }
    @Scheduled(cron = "0 05 8 * * ?", zone = "Asia/Ho_Chi_Minh") // Lên lịch chạy mỗi ngày lúc 0:00 AM
    public void scheduleLoadData() {
        System.out.println("Scheduled task started: Loading data from staging to DW...");
        loadDataFromStagingToDW();
    }
    public void loadDataFromStagingToDW() {

        // 1. Kiểm tra nếu dữ liệu từ staging đã được load vào data warehouse hôm nay
        if (controlLogService.isTodayLogStatus("Load Data From Staging to Data Warehouse", "Complete")) {
        /*
            1.1. Nếu đã load => Insert 1 dòng vào control.logs với status="Failed"
                 và message="Load data to data warehouse(Loaded)"
         */
            controlLogService.insertLog("Load data to data warehouse(Loaded)", "Failed", 0);
            System.out.println("Data from staging to DW has already been loaded today.");
            return;
        }

    /*
        2. Kết nối database staging
        3. Kết nối database data warehouse
        4. Insert 1 dòng vào control.logs với status="Running"
           và message="Load data from staging to data warehouse"
     */
        Log runningLog = controlLogService.insertLog("Load Data From Staging to Data Warehouse", "Running", 0);

        try {
        /*
            5. Thực thi stored procedure trong SQL để chuyển dữ liệu từ staging sang data warehouse
         */
            dwJdbcTemplate.execute("CALL LoadDataFromStagingToDW()");

            // 6. Đếm số lượng bản ghi đã được insert vào bảng trong DW (vd: bảng `bikes`)
            String countSql = "SELECT COUNT(*) FROM bikes";
            int quantity = dwJdbcTemplate.queryForObject(countSql, Integer.class);

            // 7. Cập nhật log với trạng thái thành công và số lượng bản ghi
            controlLogService.updateLogToSuccessful(runningLog.getId(), quantity);
            emailService.sendEmailNotification(
                    "xuanthuc254@gmail.com",
                    "Data Load Successful",
                    "Data successfully loaded from Staging to DW. Total records: " + quantity
            );




            System.out.println("Data successfully loaded from Staging to DW with quantity: " + quantity);
            System.out.println("Data successfully loaded from Staging to DW.");
        } catch (Exception e) {
            // 8. Nếu có lỗi, cập nhật log với trạng thái thất bại và in ra thông báo lỗi
            System.out.println("Error loading data: " + e.getMessage());
            controlLogService.updateLogToFailed(runningLog.getId());
            emailService.sendEmailNotification(
                    "xuanthuc254@gmail.com",
                    "Data Load Failed",
                    "Error loading data from Staging to DW: " + e.getMessage()
            );
        }
    }

}
