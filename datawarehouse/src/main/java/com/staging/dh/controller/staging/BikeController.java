package com.staging.dh.controller.staging;

import com.staging.dh.model.staging.Bike;
import com.staging.dh.responseForm.ResponseObject;
import com.staging.dh.service.staging.IBikeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@CrossOrigin
@RestController
@RequestMapping("/api/bike")
public class BikeController {
    @Autowired
    private IBikeService service;

    @PostMapping("/add")
    public ResponseEntity<ResponseObject> add(@RequestBody Bike bike){

        System.out.println(bike);
        service.add(bike);

        return ResponseEntity.status(HttpStatus.OK).body(
                new ResponseObject("Success", "Save success", bike)
        );
    }
}
