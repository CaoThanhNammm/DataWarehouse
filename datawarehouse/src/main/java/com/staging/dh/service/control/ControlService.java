package com.staging.dh.service.control;

import com.staging.dh.model.control.Control;
import com.staging.dh.repository.control.ControlRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ControlService implements IControllerService {
    @Autowired
    private ControlRepo dao;


    @Override
    public void add(Control control) {
        control.setKeyword(control.getKeyword().trim());
        if(!dao.existsByKeyword(control.getKeyword())){
            dao.save(control);
        }
    }

    @Override
    public Control increaseScrapeTimes(int id) {
        Control control = dao.findById(id).orElseThrow();
        control.setScrapeTimes(control.getScrapeTimes() + 1);
        dao.save(control);
        return control;
    }

    @Override
    public Control getIdByKeyword(String keyword) {
        return dao.findByKeyword(keyword);
    }
}
