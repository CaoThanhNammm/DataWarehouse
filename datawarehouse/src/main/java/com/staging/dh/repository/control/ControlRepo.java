package com.staging.dh.repository.control;


import com.staging.dh.model.control.Control;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;


@Repository
public interface ControlRepo extends JpaRepository<Control, Integer> {
    Control findByKeyword(String keyword);

    boolean existsByKeyword(String keyword);
}
