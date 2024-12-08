package org.example.dw21130558_mxt.model.control;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@ToString
@Setter
@Table(name = "config")
@Entity
public class Config {
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
