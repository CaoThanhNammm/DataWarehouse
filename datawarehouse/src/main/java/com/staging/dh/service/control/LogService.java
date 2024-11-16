package com.staging.dh.service.control;

import com.staging.dh.config.Constant;
import com.staging.dh.model.control.Log;
import com.staging.dh.repository.control.LogRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class LogService implements ILogService {
    @Autowired
    private LogRepo dao;

    @Override
    public Log add(Log log) {
        if (log.getStatus().getId() != Constant.WAITING) {
            dao.save(log);
            return log;
        }

        if (!dao.existsByWebsiteIdAndStatus(log.getWebsiteId(), log.getStatus())) {
            dao.save(log);
            return log;
        }
        return null;
    }
}
