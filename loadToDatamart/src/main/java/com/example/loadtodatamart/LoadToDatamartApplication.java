package com.example.loadtodatamart;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class LoadToDatamartApplication {

    public static void main(String[] args) {
        SpringApplication.run(LoadToDatamartApplication.class, args);
    }

    @Bean
    public CommandLineRunner commandLineRunner(ApplicationContext context) {
        return args -> {
            // Thực hiện tác vụ của bạn tại đây, ví dụ: tải dữ liệu vào data mart
            System.out.println("Tác vụ đã hoàn thành!");

            // Dừng ứng dụng sau khi hoàn thành tác vụ
            SpringApplication.exit(context, () -> 0);  // 0 là mã thoát (thành công)
        };
    }
}
