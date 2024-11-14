package com.staging.dh.controller.control;

import com.staging.dh.model.control.Config;
import com.staging.dh.responseForm.ResponseObject;
import com.staging.dh.service.control.IControllerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/control")
public class ConfigController {

    @Autowired
    private IControllerService service;

    @GetMapping("/findAll")
    public ResponseEntity<ResponseObject> findAll(){
        List<Config> configs = service.findAll();

        return ResponseEntity.status(HttpStatus.OK).body(
                new ResponseObject("Success", "Get all website success", configs)
        );
    }

    @GetMapping("/get/{key}")
    public ResponseEntity<ResponseObject> getIdByKeyword(@PathVariable(name = "key") String keyword){
        Config config = service.getIdByKeyword(keyword);

        return ResponseEntity.status(HttpStatus.OK).body(
                new ResponseObject("Success", "Add success", config)
        );
    }

    @PostMapping("/add")
    public ResponseEntity<ResponseObject> add(@RequestBody Config config){
        service.add(config);

        return ResponseEntity.status(HttpStatus.OK).body(
                new ResponseObject("Success", "Add success", config)
        );
    }

    @PutMapping("/increase/{id}")
    public ResponseEntity<ResponseObject> increase(@PathVariable int id){
        Config config = service.increaseScrapeTimes(id);

        return ResponseEntity.status(HttpStatus.OK).body(
                new ResponseObject("Success", "Add success", config)
        );
    }
}
