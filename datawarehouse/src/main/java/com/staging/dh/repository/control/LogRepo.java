package com.staging.dh.repository.control;


import com.staging.dh.model.control.Control;
import com.staging.dh.model.control.Log;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;

@Repository
public interface LogRepo extends JpaRepository<Log, Integer> {
}
