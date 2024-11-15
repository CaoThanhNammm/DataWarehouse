package com.staging.dh.service.control;

import com.staging.dh.model.control.Log;
import com.staging.dh.repository.control.LogRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class LogService implements ILogService{
    @Autowired
    private LogRepo dao;

    @Override
    public Log add(Log log) {
        if(!dao.existsByWebsiteIdAndStatus(log.getWebsiteId(), log.getStatus())){
            dao.save(log);
            return log;
        }
        return null;
    }
}
