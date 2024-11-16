package org.example.dw21130558_mxt.controller.datawarehouse;

import org.example.dw21130558_mxt.service.datawarehouse.DatawarehouseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class LoadToDatawarehouseController
{
    @Autowired
    private DatawarehouseService loadDWService;

    @PostMapping("/load-data-stg")
    public String loadDataFromDWToDM() {
        loadDWService.loadDataFromStagingToDW();
        return "Data load process started.";
    }
}
