import config
import scrape_xedapgiakho
import scrape_bike2school
import API
from controller.control import ConfigController, LogController, StatusController
import threading
import time


def runConfig():
    print(config.delete_all_bikes())
    print(config.set_all_website_waiting())
    print(config.send_email_for_prepare(API.get_subject_email(), API.create_message_for_email(API.get_message_waiting())))


def runScrapeXedapGiaKho():
    # lấy url của website xepdapgiakho
    url = ConfigController.getIdByKeyword(f"{API.get_context_config()}/get", API.get_keyword_xedapgiakho())["website"]
    scrape_xedapgiakho.general_xedapgiakho(url)


def runScrapeBike2school():
    # lấy url của website bike2schol
    website = ConfigController.getIdByKeyword(f'{API.get_context_config()}/get', API.get_keyword_bike2school())[
        'website']
    scrape_bike2school.general_bike2school(website)

def isShouldRunningBike2school():
    websiteBike2school = ConfigController.getIdByKeyword(f"{API.get_context_config()}/get",
                                                         API.get_keyword_bike2school())
    id_website_bike_2_school = websiteBike2school["id"]

    logJsonRunning = {
        "websiteId": {
            "id": id_website_bike_2_school
        },
        "status": {
            "id":
                StatusController.getStatusByName(f"{API.get_context_status()}/getStatusByName",
                                                 API.get_type_complete())[
                    "id"]
        }
    }
    isShouldRunning = LogController.isShouldRunning(f"{API.get_context_log()}/isShouldRunning", logJsonRunning)

    if not isShouldRunning:
        runScrapeBike2school()


def isShouldRunningXedapgiakho():
    websiteXedapgiakho = ConfigController.getIdByKeyword(f"{API.get_context_config()}/get",
                                                         API.get_keyword_xedapgiakho())

    id_website_xe_dap_gia_kho = websiteXedapgiakho["id"]

    logJsonRunning = {
        "websiteId": {
            "id": id_website_xe_dap_gia_kho
        },
        "status": {
            "id":
                StatusController.getStatusByName(f"{API.get_context_status()}/getStatusByName",
                                                 API.get_type_complete())[
                    "id"]
        }
    }
    isShouldRunning = LogController.isShouldRunning(f"{API.get_context_log()}/isShouldRunning", logJsonRunning)

    if not isShouldRunning:
        runScrapeXedapGiaKho()


def isShouldRunningForConfig():
    websiteXedapgiakho = ConfigController.getIdByKeyword(f"{API.get_context_config()}/get",
                                                         API.get_keyword_xedapgiakho())

    id_website_xe_dap_gia_kho = websiteXedapgiakho["id"]

    logJsonRunning = {
        "websiteId": {
            "id": id_website_xe_dap_gia_kho
        },
        "status": {
            "id":
                StatusController.getStatusByName(f"{API.get_context_status()}/getStatusByName",
                                                 API.get_type_waiting())[
                    "id"]
        }
    }
    isShouldRunning = LogController.isShouldRunning(f"{API.get_context_log()}/isShouldRunning", logJsonRunning)

    if not isShouldRunning:
        print("CONFIG CHẠY 1 LẦN DUY NHẤT TRONG NGÀY")
        runConfig()
        return

    print("CONFIG ĐÃ CHẠY RỒI")
def runAll():
    # config chỉ chạy 1 lần trong ngày
    isShouldRunningForConfig()


    # trang web nào bị lỗi thì chạy, thành công thì không chạy nữa
    thread1 = threading.Thread(target=isShouldRunningBike2school)
    thread2 = threading.Thread(target=isShouldRunningXedapgiakho)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

runAll()