package org.example.dw21130558_mxt.repository.control;


import org.example.dw21130558_mxt.model.control.Log;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.Optional;

@Repository
public interface LogRepo extends JpaRepository<Log, Integer> {

    Optional<Log> findFirstByMessageAndStatus_NameAndTimeStartAfter(
            String message, String statusName, LocalDateTime timeStart);

}
