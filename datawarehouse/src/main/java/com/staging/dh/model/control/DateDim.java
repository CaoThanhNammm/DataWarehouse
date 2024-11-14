package com.staging.dh.model.control;

import jakarta.persistence.*;
import lombok.Getter;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Getter
@Entity
@Table(name = "dateDim")
public class DateDim {
    @Id
    @Column
    private int dateSk;
    @Column
    private LocalDate fullDate;
    @Column
    private int daySince2005;
    @ManyToOne
    @JoinColumn(name = "monthSince2005")
    private MonthDim monthSince2005;
    @Column
    private String dayOfWeek;
    @Column
    private String calendarMonth;
    @Column
    private int calendarYear;
    @Column
    private String calendarYearMonth;
    @Column
    private int dayOfMonth;
    @Column
    private int DayOfYear;
    @Column
    private int weekOfYearSunday;
    @Column
    private String yearWeekSunday;
    @Column
    private String weekSundayStart;
    @Column
    private String weekOfYearMonday;
    @Column
    private String weekMondayStart;
    @Column
    private String quarterSince2005;
    @Column
    private int quarterOfYear;
    @Column
    private String holiday;
    @Column
    private String dayType;
}
