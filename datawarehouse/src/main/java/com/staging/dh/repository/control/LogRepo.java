package com.staging.dh.repository.control;


import com.staging.dh.model.control.Log;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface LogRepo extends JpaRepository<Log, Integer> {
}
