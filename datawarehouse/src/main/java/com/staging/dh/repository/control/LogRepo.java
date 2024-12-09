package com.staging.dh.repository.control;


import com.staging.dh.model.control.Config;
import com.staging.dh.model.control.DateDim;
import com.staging.dh.model.control.Log;
import com.staging.dh.model.control.Status;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;

@Repository
public interface LogRepo extends JpaRepository<Log, Integer> {

    boolean existsByWebsiteIdAndTimeStartAndStatus(Config website, LocalDate today, Status status);
}
