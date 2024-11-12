package com.staging.dh.repository.control;

import com.staging.dh.model.control.DateDim;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
@Repository
public interface DateDimRepo extends JpaRepository<DateDim, Integer> {
    DateDim findByFullDate(LocalDate fullDate);
}
