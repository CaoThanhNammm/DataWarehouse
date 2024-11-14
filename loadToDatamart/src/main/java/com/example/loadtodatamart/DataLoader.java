package com.example.loadtodatamart;


import com.example.loadtodatamart.service.datamart.DataMartService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataLoader implements CommandLineRunner {

    @Autowired
    private DataMartService dataMartService;

    @Override
    public void run(String... args) throws Exception {
        // Gọi phương thức load dữ liệu từ DW vào DM
        dataMartService.loadDataFromDWToDM();
    }
}
