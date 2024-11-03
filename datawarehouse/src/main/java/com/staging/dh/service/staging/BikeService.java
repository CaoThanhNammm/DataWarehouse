package com.staging.dh.service.staging;


import com.staging.dh.model.staging.Bike;
import com.staging.dh.repository.staging.BikeRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class BikeService implements IBikeService {
    @Autowired
    private BikeRepo dao;

    @Override
    public void add(Bike bike) {
        dao.save(bike);
    }

    @Override
    public void deleteAll() {
        dao.deleteAll();
    }
}
