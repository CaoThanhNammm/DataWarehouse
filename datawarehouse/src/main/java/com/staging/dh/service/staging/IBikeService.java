package com.staging.dh.service.staging;


import com.staging.dh.model.staging.Bike;

public interface IBikeService {
    void add(Bike bike);
    void deleteAll();
}
