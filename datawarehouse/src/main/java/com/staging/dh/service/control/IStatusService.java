package com.staging.dh.service.control;

import com.staging.dh.model.control.Status;

public interface IStatusService {
    void add(Status status);
    Status getStatusByName(String name);
}
