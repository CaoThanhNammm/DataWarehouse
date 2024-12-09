package com.staging.dh.service.control;

import com.staging.dh.model.control.Log;
import com.staging.dh.model.control.Status;

import java.time.LocalDate;

public interface ILogService {
    Log add(Log log);
    boolean isShouldRunning(Log log);
}
