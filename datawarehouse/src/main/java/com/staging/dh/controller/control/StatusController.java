package com.staging.dh.controller.control;

import com.staging.dh.model.control.Status;
import com.staging.dh.responseForm.ResponseObject;
import com.staging.dh.service.control.ILogService;
import com.staging.dh.service.control.IStatusService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/status")
public class StatusController {
    @Autowired
    private IStatusService service;

    @GetMapping("/getStatusByName/{name}")
    public ResponseEntity<ResponseObject> getStatusByName(@PathVariable String name){
        Status status = service.getStatusByName(name);
        if(status != null){
            return ResponseEntity.status(HttpStatus.OK).body(
                    new ResponseObject("Success", "Get status success", status)
            );
        }

        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(
                new ResponseObject("Failed", "Get status failed", null)
        );
    }


    @PostMapping("/add")
    public ResponseEntity<ResponseObject> add(@RequestBody Status status){
        service.add(status);

        return ResponseEntity.status(HttpStatus.OK).body(
                new ResponseObject("Success", "Add success", status)
        );
    }
}
