package org.example.dw21130558_mxt.repository.control;



import org.example.dw21130558_mxt.model.control.Config;
import org.springframework.stereotype.Repository;
import org.springframework.data.jpa.repository.JpaRepository;


@Repository
public interface ControlRepo extends JpaRepository<Config, Integer> {

}