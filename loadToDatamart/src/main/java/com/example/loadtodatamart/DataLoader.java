package com.example.loadtodatamart;


import com.example.loadtodatamart.service.datamart.DataMartService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Component;

@Component
public class DataLoader implements CommandLineRunner {

    @Autowired
    private DataMartService dataMartService;

    @Autowired
    private ApplicationContext appContext;

    @Override
    public void run(String... args) throws Exception {
        try {
            if (!dataMartService.isDataLoaded()) {
                dataMartService.loadDataFromDWToDM();
            } else {
                System.out.println("Dữ liệu đã được tải trước đó. Không cần thực hiện lại.");
            }
        } finally {
            SpringApplication.exit(appContext, () -> 0);
        }
    }
}

