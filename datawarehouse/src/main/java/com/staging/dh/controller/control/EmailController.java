package com.staging.dh.controller.control;

import com.staging.dh.repository.control.Email;
import com.staging.dh.responseForm.ResponseObject;
import com.staging.dh.service.control.IEmailService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/email")
public class EmailController {
    @Autowired
    private IEmailService service;

    @GetMapping("/send")
    public ResponseEntity<ResponseObject> sendEmail(@RequestParam String receiver, @RequestParam String subject, @RequestParam String message) {
        Email emailSent = service.sendEmailNotification(receiver, subject, message);

        return ResponseEntity.status(HttpStatus.OK).body(
                new ResponseObject("Success", "Send mail success", emailSent)
        );
    }

}
