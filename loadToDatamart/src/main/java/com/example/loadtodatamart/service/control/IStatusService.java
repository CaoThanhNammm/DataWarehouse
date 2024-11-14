package com.example.loadtodatamart.service.control;

import com.example.loadtodatamart.model.control.Status;

public interface IStatusService {
    void add(Status status);
    Status getStatusByName(String name);
}
