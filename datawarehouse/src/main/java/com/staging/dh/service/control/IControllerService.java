package com.staging.dh.service.control;

import com.staging.dh.model.control.Control;

public interface IControllerService {
    void add(Control control);
    Control increaseScrapeTimes(int id);
    Control getIdByKeyword(String website);

}
