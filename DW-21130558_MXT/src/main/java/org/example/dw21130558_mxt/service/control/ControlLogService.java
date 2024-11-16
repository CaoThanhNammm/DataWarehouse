package org.example.dw21130558_mxt.service.control;


import org.example.dw21130558_mxt.model.control.Log;
import org.example.dw21130558_mxt.model.control.Status;
import org.example.dw21130558_mxt.repository.control.LogRepo;
import org.example.dw21130558_mxt.repository.control.StatusRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.Optional;

@Service
public class ControlLogService implements ILogService {


    @Autowired
    private LogRepo logRepository;

    @Autowired
    private StatusRepo statusRepository;

    /**
     * Ghi log với thông tin chi tiết.
     *
     * @return
     */
    @Override
    public Log insertLog(String message, String statusName, int quantity) {
        Status status = statusRepository.findByName(statusName);
        Log log = new Log(message, status);
        log.setTimeStart(LocalDateTime.now());
        log.setQuantity(quantity);
        logRepository.save(log);
        System.out.println("Inserted log: " + log.getMessage() + " with status: " + log.getStatus().getName());
        return log;
    }
    /**
     * Kiểm tra log của ngày hôm nay với message và statusName đã tồn tại hay chưa.
     */
    public boolean isTodayLogStatus(String message, String statusName) {
        LocalDate today = LocalDate.now();
        System.out.println("Checking log for: " + message + " with status: " + statusName);
        Optional<Log> log = logRepository.findFirstByMessageAndStatus_NameAndTimeStartAfter(
                message, statusName, today.atStartOfDay()
        );
        return log.isPresent();
    }

    public void updateLogToSuccessful(int logId, int quantity) {
        Optional<Log> logOptional = logRepository.findById(logId);
        if (logOptional.isPresent()) {
            Log log = logOptional.get();
            log.setStatus(statusRepository.findByName("Complete"));
            log.setQuantity(quantity);
            log.setTimeEnd(LocalDateTime.now());
            logRepository.save(log);
            System.out.println("Log updated to Successful with quantity: " + quantity);
        }
    }

    public void updateLogToFailed(int logId) {
        Optional<Log> logOptional = logRepository.findById(logId);
        if (logOptional.isPresent()) {
            Log log = logOptional.get();
            log.setStatus(statusRepository.findByName("Failed"));
            log.setTimeEnd(LocalDateTime.now());
            logRepository.save(log);
            System.out.println("Log updated to Failed.");
        }
    }

}
