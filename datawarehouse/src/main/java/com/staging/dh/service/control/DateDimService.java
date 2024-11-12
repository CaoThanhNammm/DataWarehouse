package com.staging.dh.service.control;

import com.staging.dh.repository.control.DateDimRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;

@Service
public class DateDimService implements IDateDimService{
    @Autowired
    private DateDimRepo dao;

    @Override
    public int getIdDateDim(LocalDate today) {
        return dao.findByFullDate(today).getDateSk();
    }
}
