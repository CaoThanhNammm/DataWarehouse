package com.example.loadtodatamart.service.control;

import com.example.loadtodatamart.model.control.Log;

public interface ILogService {
    Log insertLog(String message, String statusName, int quantity);
}
