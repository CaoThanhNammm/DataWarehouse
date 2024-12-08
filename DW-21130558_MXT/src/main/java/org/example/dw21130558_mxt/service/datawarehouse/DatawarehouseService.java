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
            @Autowired
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

            public void loadDataFromStagingToDW() {
                String recipient = "xuanthuc254@gmail.com";

                // Kiểm tra nếu dữ liệu scrape hôm nay đã hoàn thành
                if (!controlLogService.isTodayLogStatus("complete scrape data", "Complete")) {
                    controlLogService.insertLog("Load Data From Staging to Data Warehouse", "Failed", 0);
                    System.out.println("Dữ liệu từ staging ngày hôm nay chưa được scrape hoàn thành.");
                    return;
                }

                // Kiểm tra nếu dữ liệu từ staging đã được load vào data warehouse hôm nay
                if (controlLogService.isTodayLogStatus("Load Data From Staging to Data Warehouse", "Complete")) {
                    // Nếu đã load => Insert 1 dòng vào control.logs với status="Failed"
                    // và message="Load data to data warehouse(Loaded)"
                    controlLogService.insertLog("Load Data From Staging to Data Warehouse", "Failed", 0);
                    System.out.println("Data from staging to DW has already been loaded today.");
                    return;
                }

                // Kết nối database và thực hiện quy trình load dữ liệu
                Log runningLog = controlLogService.insertLog("Load Data From Staging to Data Warehouse", "Running", 0);
                try {
                    System.out.println("Log Running inserted successfully.");
                } catch (Exception ex) {
                    System.out.println("Error inserting Running log: " + ex.getMessage());
                }

                try {
                    // Thực thi stored procedure trong SQL để chuyển dữ liệu từ staging sang data warehouse
                    dwJdbcTemplate.execute("CALL LoadDataFromStagingToDW2()");

                    // Đếm số lượng bản ghi đã được insert vào bảng trong DW (vd: bảng `product_dim`)
                    String countSql = "SELECT COUNT(*) FROM datawarehouse.dim_bikes_processed;";
                    int quantity = dwJdbcTemplate.queryForObject(countSql, Integer.class);

                    // Cập nhật log với trạng thái thành công và số lượng bản ghi
                    controlLogService.updateLogToSuccessful(runningLog.getId(), quantity);

                    String subject = "Quy trình load dữ liệu từ stg vào dw ngày hôm nay đã hoàn tất";
                    String body = "Quy trình load dữ liệu từ stg vào dw ngày hôm nay đã hoàn tất thành công. Số bản ghi insert vào dw là " + quantity + "\n\nTrân trọng,\nHệ thống";
                    emailService.sendEmail(recipient, subject, body);

                    System.out.println("Data successfully loaded from Staging to DW with quantity: " + quantity);
                } catch (Exception e) {
                    // Nếu có lỗi, cập nhật log với trạng thái thất bại và in ra thông báo lỗi
                    System.out.println("Error loading data: " + e.getMessage());
                    controlLogService.updateLogToFailed(runningLog.getId());
                }
            }

        }
