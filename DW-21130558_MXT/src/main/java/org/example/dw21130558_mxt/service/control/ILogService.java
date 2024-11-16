package org.example.dw21130558_mxt.service.control;


import org.example.dw21130558_mxt.model.control.Log;

public interface ILogService {
    Log insertLog(String message, String statusName, int quantity);
}
