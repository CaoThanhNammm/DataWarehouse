import time
from datetime import datetime, date
from selenium.webdriver.common.by import By
import pandas as pd
import API
import general
from controller.control import ConfigController, LogController, StatusController, DateDimController, EmailController
from controller.staging import BikeController

def delete_all_bikes():
    return BikeController.deleteAll(f'{API.get_context_bike()}/deleteAll')

def set_all_website_waiting():
    # lay ra tat ca id
    websites = ConfigController.findAll(f'{API.get_context_config()}/findAll')
    # lấy ra id của datedim hôm nay
    dateDimJson = {
        "fullDate": general.get_local_date()
    }
    dateSk = DateDimController.getIdToday(f"{API.get_context_dateDim()}/id", dateDimJson)

    for website in websites:
        website_id = website["id"]
        print(website_id)
        logJson = {
            "message": API.get_message("waitingMessage"),
            "websiteId": {
                "id": website_id
            },
            'status': {
                "id":
                    StatusController.getStatusByName(f"{API.get_context_status()}/getStatusByName",
                                                     API.get_type_waiting())["id"]
            },
            'dateSk': {
                'dateSk': dateSk
            }
        }
        LogController.add(f"{API.get_context_log()}/add", logJson)


def send_email_for_prepare(subject, message):
    res = EmailController.send(f'{API.get_context_email()}/send', API.get_receiver_email(), subject, message)
    return res

print(delete_all_bikes())
print(set_all_website_waiting())
print(send_email_for_prepare("Hệ Thống Báo Giá Xe Đạp", API.create_message_for_email(API.get_message_waiting())))

