package com.example.loadtodatamart.repository.control;


import com.example.loadtodatamart.model.control.Control;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


@Repository
public interface ControlRepo extends JpaRepository<Control, Integer> {

}
