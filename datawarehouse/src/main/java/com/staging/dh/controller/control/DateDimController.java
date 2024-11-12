package com.staging.dh.controller.control;

import com.staging.dh.model.control.DateDim;
import com.staging.dh.responseForm.ResponseObject;
import com.staging.dh.service.control.IDateDimService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/dateDim")
public class DateDimController {
    @Autowired
    private IDateDimService service;

    @GetMapping("/id")
    public ResponseEntity<ResponseObject> getIdByDate(@RequestBody DateDim dateDim){
        System.out.println(dateDim);

        int id = service.getIdDateDim(dateDim.getFullDate());

        return ResponseEntity.status(HttpStatus.OK).body(
                new ResponseObject("Success", "Get id today success", id)
        );
    }
}
