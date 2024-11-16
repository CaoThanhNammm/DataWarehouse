package org.example.dw21130558_mxt.service.control;


import org.example.dw21130558_mxt.model.control.Status;

public interface IStatusService {
    void add(Status status);
    Status getStatusByName(String name);
}
