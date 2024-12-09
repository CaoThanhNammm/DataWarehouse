package com.staging.dh.controller.control;

import com.staging.dh.model.control.Log;
import com.staging.dh.responseForm.ResponseObject;
import com.staging.dh.service.control.ILogService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/log")
public class LogController {
    @Autowired
    private ILogService service;

    @PostMapping("/add")
    public ResponseEntity<ResponseObject> add(@RequestBody Log log) {
        Log logInserted = service.add(log);

        if (logInserted != null) {
            return ResponseEntity.status(HttpStatus.OK).body(
                    new ResponseObject("Success", "Add success", log)
            );
        }
        return ResponseEntity.status(HttpStatus.OK).body(
                new ResponseObject("Failed", "Add failed", log)
        );
    }

    @GetMapping("/isShouldRunning")
    public ResponseEntity<ResponseObject> isShouldRunning(@RequestBody Log log) {
        boolean isShouldRunning = service.isShouldRunning(log);
        return ResponseEntity.status(HttpStatus.OK).body(
                new ResponseObject("Success", "Is should running", isShouldRunning)
        );
    }
}
