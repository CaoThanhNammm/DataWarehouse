package com.example.loadtodatamart.repository.control;



import com.example.loadtodatamart.model.control.Control;
import com.example.loadtodatamart.model.control.Log;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.Optional;

@Repository
public interface LogRepo extends JpaRepository<Log, Integer> {

    Optional<Log> findFirstByMessageAndStatus_NameAndTimeStartAfter(
            String message, String statusName, LocalDateTime timeStart);

}
