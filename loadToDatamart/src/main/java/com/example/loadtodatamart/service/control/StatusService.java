package com.example.loadtodatamart.service.control;

import com.example.loadtodatamart.model.control.Status;
import com.example.loadtodatamart.repository.control.StatusRepo;
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
