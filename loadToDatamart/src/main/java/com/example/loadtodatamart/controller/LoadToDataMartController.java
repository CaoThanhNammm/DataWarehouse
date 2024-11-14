package com.example.loadtodatamart.controller;

import com.example.loadtodatamart.service.datamart.DataMartService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LoadToDataMartController {

    @Autowired
    private DataMartService loadDataMartService;

    @PostMapping("/load-data")
    public String loadDataFromDWToDM() {
        loadDataMartService.loadDataFromDWToDM();
        return "Data load process started.";
    }
}

