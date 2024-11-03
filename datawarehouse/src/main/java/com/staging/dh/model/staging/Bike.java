package com.staging.dh.model.staging;

import jakarta.persistence.*;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import java.time.LocalDateTime;

@Getter
@ToString
@EqualsAndHashCode
@Setter
@Table(name = "bikes")
@Entity
public class Bike {
    @Column(name = "naturalId")
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int naturalId;

    @Column
    private String id;

    @Column
    private String name;
    @Column
    private String price;
    @Column(name = "priceSale")
    private String priceSale;
    @Column
    private String brand;
    @Column
    private String color;
    @Column
    private String size;
    @Column
    private String description_part1;
    @Column
    private String description_part2;
    @Column
    private String description_part3;
    @Column
    private String status;
    @Column
    private LocalDateTime timeStartScrape;
    @Column
    private LocalDateTime  timeEndScrape;
    @Column
    private LocalDateTime timeStartInsert;

    @PrePersist
    public void prePersist() {
        timeStartInsert = LocalDateTime.now();
    }
}