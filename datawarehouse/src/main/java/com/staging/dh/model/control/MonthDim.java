package com.staging.dh.model.control;

import jakarta.persistence.*;

@Entity
@Table(name = "monthDim")
public class MonthDim {
    @Column
    @Id
    private int monthSk;
    @Column
    private String calendarYearMonth;
    @Column
    private int monthSince2005;
    @Column
    private int dateSkStart;
    @Column
    private int dateSkEnd;
}
