package com.staging.dh.repository.control;

import lombok.*;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class Email {
    private String sender;
    private String receiver;
    private String subject;
    private String message;
}
