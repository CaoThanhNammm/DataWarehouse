package org.example.dw21130558_mxt.service.control;


import org.example.dw21130558_mxt.model.control.Status;
import org.example.dw21130558_mxt.repository.control.StatusRepo;
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
