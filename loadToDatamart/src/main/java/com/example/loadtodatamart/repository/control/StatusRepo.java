package com.example.loadtodatamart.repository.control;


import com.example.loadtodatamart.model.control.Status;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface StatusRepo extends JpaRepository<Status, Integer> {
    Status findByName(String name);
}
