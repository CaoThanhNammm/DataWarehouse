package com.staging.dh.service.control;

import com.staging.dh.repository.control.Email;

public interface IEmailService {

    Email sendEmailNotification(String receiver, String subject, String message);
}
