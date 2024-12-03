package org.example.dw21130558_mxt.responseForm;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@AllArgsConstructor
@Getter
@Setter
public class ResponseObject {
    private String status;
    private String message;
    private Object data;
}
