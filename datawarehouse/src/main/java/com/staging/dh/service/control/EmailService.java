package com.staging.dh.service.control;

import com.staging.dh.repository.control.Email;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.experimental.NonFinal;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

@Service
@Slf4j
@Data
@RequiredArgsConstructor
public class EmailService implements IEmailService{
    @Autowired
    private JavaMailSender mailSender;

    @NonFinal
    @Value("${spring.mail.username}")
    private String FROM_EMAIL;

    @Override
    public Email sendEmailNotification(String receiver, String subject, String content) {
        SimpleMailMessage message = new SimpleMailMessage();
        message.setTo(receiver);
        message.setSubject(subject);
        message.setText(content);
        message.setFrom(FROM_EMAIL);

        mailSender.send(message);
        return new Email(FROM_EMAIL, receiver, "Thông báo lấy dữ liệu", content);
    }
}
