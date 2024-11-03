package com.staging.dh.model.control;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.time.LocalDateTime;

@Getter
@ToString
@Setter
@Table(name = "control")
@Entity
public class Control {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;
    @Column(name = "website")
    private String website;

    @Column
    private String keyword;

    @Column
    private String saveFolder;

    @Column(name="scrapeTimes")
    private int scrapeTimes;

    @PrePersist
    public void prePersist() {
        scrapeTimes = 0;
    }
}
