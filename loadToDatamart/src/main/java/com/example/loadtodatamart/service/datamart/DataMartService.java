package com.example.loadtodatamart.service.datamart;

import com.example.loadtodatamart.model.control.Log;
import com.example.loadtodatamart.service.control.ControlLogService;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

@Service
public class DataMartService {

    @Autowired
    private ControlLogService controlLogService;

    private final JdbcTemplate dwJdbcTemplate;
    private final JdbcTemplate dmJdbcTemplate;

    private boolean isDataLoaded = false;

    @Autowired
    public DataMartService(JdbcTemplate dwJdbcTemplate, JdbcTemplate dmJdbcTemplate) {
        this.dwJdbcTemplate = dwJdbcTemplate;
        this.dmJdbcTemplate = dmJdbcTemplate;
    }

    @PostConstruct
    public void init() {
        // Gọi phương thức load dữ liệu từ DW vào DM
        if (!isDataLoaded) {
            loadDataFromDWToDM();
            isDataLoaded = true;  // Đánh dấu rằng dữ liệu đã được tải
        }
    }

    public void loadDataFromDWToDM() {

//        1. Load những biến trong file appliation.properties
//        2. Kêt nối database control
//        3.Kiểm tra đã load data từ staging vào datawarehouse hay chưa
        if (!controlLogService.isTodayLogStatus("Load Data From Staging to Data Warehouse", "Complete")) {
             /*
                3.1. Nếu chưa load =>Insert 1 dòng vào control.logs với status="Failed" and messagage="Load data to datamart(can not run)"
            */
            controlLogService.insertLog("Load data to datamart(can not run)", "Failed", 0);
             /*
                3.2. Đóng kết nối database
            */
            return;
        }

        /*
            4. Kiểm tra hôm nay đã load data từ warehouse vào data mart
        */
        if (controlLogService.isTodayLogStatus("Load data to datamart", "Complete")) {
             /*
                4.1. Nếu đã load rồi=> Insert 1 dòng vào control.logs với status="Failed" and message="Load data to datamart(Loaded)"
            */
//            controlLogService.insertLog("Load data to datamart(Loaded)", "Failed", 0);
            System.out.println("Data load already in progress or completed today.");
            return;
        }

         /*
            5. kết nối database datawarehouse
            6. Kết nối database datamart
            7. Insert 1 dòng vào control.logs với status="Running" and massage="Load data to datamart"
         */
        Log runningLog = controlLogService.insertLog("Load data to datamart", "Running", 0);

        try {

         /*
           Từ 8- End ( xử lí trong proc bên sql )
         */
            dmJdbcTemplate.execute("CALL LoadDataFromDWToDM()");
            // Đếm số lượng bản ghi đã được insert vào bảng product trong DM
            String countSql = "SELECT COUNT(*) FROM product";
            int quantity = dmJdbcTemplate.queryForObject(countSql, Integer.class);

            // In ra số lượng bản ghi đã insert vào bảng product
            controlLogService.updateLogToSuccessful(runningLog.getId(), quantity);
            System.out.println("Data successfully loaded from DW to DM with quantity: " + quantity);
            System.out.println("Data successfully loaded from DW to DM.");
            // Đóng tất cả kết nối khi tải thành công
            return;
        } catch (Exception e) {
            System.out.println("Error loading data: " + e.getMessage());
            controlLogService.updateLogToFailed(runningLog.getId());
            return;
        }
    }
}
