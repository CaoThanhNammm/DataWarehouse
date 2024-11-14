package com.staging.dh.service.control;

import com.staging.dh.model.control.Config;
import com.staging.dh.repository.control.ControlRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ControlService implements IControllerService {
    @Autowired
    private ControlRepo dao;


    @Override
    public void add(Config config) {
        config.setKeyword(config.getKeyword().trim());
        if(!dao.existsByKeyword(config.getKeyword())){
            dao.save(config);
        }
    }

    @Override
    public Config increaseScrapeTimes(int id) {
        Config config = dao.findById(id).orElseThrow();
        config.setScrapeTimes(config.getScrapeTimes() + 1);
        dao.save(config);
        return config;
    }

    @Override
    public Config getIdByKeyword(String keyword) {
        return dao.findByKeyword(keyword);
    }

    @Override
    public List<Config> findAll() {
        return dao.findAll();
    }
}
