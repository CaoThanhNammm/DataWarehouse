package com.example.loadtodatamart.model.datamart;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;

import java.time.LocalDate;

@Getter
@Entity
@Table(name = "date")
public class Date {
    @Id
    @Column(name = "date_sk")
    private int dateSk;

    @Column(name = "full_date")
    private LocalDate fullDate;

    @Column(name = "day_since_2005")
    private int daySince2005;

    @Column(name = "day_of_week")
    private String dayOfWeek;

    @Column(name = "calendar_month")
    private String calendarMonth;

    @Column(name = "calendar_year")
    private int calendarYear;

    @Column(name = "calendar_year_month")
    private String calendarYearMonth;

    @Column(name = "day_of_month")
    private int dayOfMonth;

    @Column(name = "day_of_year")
    private int dayOfYear;

    @Column(name = "week_of_year_sunday")
    private int weekOfYearSunday;

    @Column(name = "year_week_sunday")
    private String yearWeekSunday;

    @Column(name = "week_sunday_start")
    private String weekSundayStart;

    @Column(name = "week_of_year_monday")
    private String weekOfYearMonday;

    @Column(name = "week_monday_start")
    private String weekMondayStart;

    @Column(name = "quarter_since_2005")
    private String quarterSince2005;

    @Column(name = "quarter_of_year")
    private int quarterOfYear;

    @Column(name = "holiday")
    private String holiday;

    @Column(name = "day_type")
    private String dayType;
}

