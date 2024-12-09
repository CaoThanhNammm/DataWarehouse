package com.example.loadtodatamart;

import com.example.loadtodatamart.service.datamart.DataMartService;
import org.springframework.beans.factory.annotation.Autowired;
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

}
