package org.example.dw21130558_mxt.controller.control;

import org.example.dw21130558_mxt.service.control.ILogService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/log")
public class LogController {

    @Autowired
    private ILogService service;

    @PostMapping("/add")
    public void add(@RequestBody String message, String statusName, int quantity){
        service.insertLog(message, statusName, quantity);
    }

}
