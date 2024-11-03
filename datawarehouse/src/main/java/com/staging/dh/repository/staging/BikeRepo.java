package com.staging.dh.repository.staging;


import com.staging.dh.model.staging.Bike;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;

@Repository
public interface BikeRepo extends JpaRepository<Bike, Integer> {
    boolean existsByName(String name);
}
