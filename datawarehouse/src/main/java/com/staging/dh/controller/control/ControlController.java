package com.staging.dh.controller.control;

import com.staging.dh.model.control.Control;
import com.staging.dh.model.control.Log;
import com.staging.dh.responseForm.ResponseObject;
import com.staging.dh.service.control.IControllerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/control")
public class ControlController {

    @Autowired
    private IControllerService service;

    @GetMapping("/get/{key}")
    public ResponseEntity<ResponseObject> getIdByKeyword(@PathVariable(name = "key") String keyword){
        Control control = service.getIdByKeyword(keyword);

        return ResponseEntity.status(HttpStatus.OK).body(
                new ResponseObject("Success", "Add success", control)
        );
    }

    @PostMapping("/add")
    public ResponseEntity<ResponseObject> add(@RequestBody Control control){
        service.add(control);

        return ResponseEntity.status(HttpStatus.OK).body(
                new ResponseObject("Success", "Add success", control)
        );
    }

    @PutMapping("/increase/{id}")
    public ResponseEntity<ResponseObject> increase(@PathVariable int id){
        Control control = service.increaseScrapeTimes(id);

        return ResponseEntity.status(HttpStatus.OK).body(
                new ResponseObject("Success", "Add success", control)
        );
    }
}
