package org.example.dw21130558_mxt;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.beans.factory.annotation.Autowired;


@SpringBootApplication

public class Dw21130558MxtApplication {
	@Autowired
	private ApplicationContext appContext;
	public static void main(String[] args) {

		SpringApplication.run(Dw21130558MxtApplication.class, args);
	}
	@Bean
	public CommandLineRunner run() {
		return args -> {
			// Code chạy một lần khi ứng dụng khởi động
			System.out.println("Task is running...");

			// Sau khi task hoàn thành, dừng ứng dụng
			SpringApplication.exit(appContext, () -> 0);
		};
	}

}

