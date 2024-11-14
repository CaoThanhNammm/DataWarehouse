package com.staging.dh.service.control;

import com.staging.dh.model.control.Config;

import java.util.List;

public interface IControllerService {
    void add(Config config);
    Config increaseScrapeTimes(int id);
    Config getIdByKeyword(String website);

    List<Config> findAll();
}
