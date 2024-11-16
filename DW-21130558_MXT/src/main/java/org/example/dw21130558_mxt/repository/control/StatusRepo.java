package org.example.dw21130558_mxt.repository.control;


import org.example.dw21130558_mxt.model.control.Status;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface StatusRepo extends JpaRepository<Status, Integer> {
    Status findByName(String name);
}
