package com.staging.dh.service.control;

import com.staging.dh.model.control.Log;
import com.staging.dh.repository.control.LogRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class LogService implements ILogService{
    @Autowired
    private LogRepo dao;

    @Override
    public void add(Log log) {
        dao.save(log);
    }
}
