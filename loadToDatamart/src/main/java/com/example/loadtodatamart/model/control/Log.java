package com.example.loadtodatamart.model.control;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.time.LocalDateTime;

@Getter
@ToString
@Setter
@Entity
@Table(name = "logs")
public class Log {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @ManyToOne
    @JoinColumn(name = "websiteId")
    private Control websiteId;

    @Column()
    private String message;

    @Column
    private Integer quantity;

    @Column(name = "timeStart")
    private LocalDateTime timeStart;

    @Column(name = "timeEnd")
    private LocalDateTime timeEnd;

    @ManyToOne
    @JoinColumn(name = "statusId")
    private Status status;

    public Log(String message,Status status) {
        this.message = message;
        this.status = status;
    }

    public Log() {
    }
}
