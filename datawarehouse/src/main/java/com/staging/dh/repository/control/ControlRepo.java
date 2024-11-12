package com.staging.dh.repository.control;


import com.staging.dh.model.control.Config;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


@Repository
public interface ControlRepo extends JpaRepository<Config, Integer> {
    Config findByKeyword(String keyword);

    boolean existsByKeyword(String keyword);
}
