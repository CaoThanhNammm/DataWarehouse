package com.staging.dh.repository.control;


import com.staging.dh.model.control.Log;
import com.staging.dh.model.control.Status;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;

@Repository
public interface StatusRepo extends JpaRepository<Status, Integer> {
    Status findByName(String name);
}
