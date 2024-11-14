package com.staging.dh.service.staging;


import com.staging.dh.model.staging.Bike;

import java.util.List;

public interface IBikeService {
    void add(Bike bike);
    void deleteAll();
}
