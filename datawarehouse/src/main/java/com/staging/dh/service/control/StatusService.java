package com.staging.dh.service.control;

import com.staging.dh.model.control.Status;
import com.staging.dh.repository.control.StatusRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class StatusService implements IStatusService{
    @Autowired
    private StatusRepo dao;

    @Override
    public void add(Status status) {
        dao.save(status);
    }

    @Override
    public Status getStatusByName(String name) {
        return dao.findByName(name);
    }
}
