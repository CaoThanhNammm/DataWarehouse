package org.example.dw21130558_mxt;



import org.example.dw21130558_mxt.service.datawarehouse.DatawarehouseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataLoader implements CommandLineRunner {

    @Autowired
    private DatawarehouseService dw;

    @Override
    public void run(String... args) throws Exception {
        // Gọi phương thức load dữ liệu từ DW vào DM
        dw.loadDataFromStagingToDW();
    }
}
