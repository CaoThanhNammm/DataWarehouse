"""
    ĐÂY LÀ LỚP CẤU HÌNH, PHẢI CHẠY ĐẦU TIÊN
"""
import API
import general
from controller.control import ConfigController, LogController, StatusController, DateDimController, EmailController
from controller.staging import BikeController

# tác dụng: xóa tất cả dữ liệu trong bảng bike
def delete_all_bikes():
    return BikeController.deleteAll(f'{API.get_context_bike()}/deleteAll')

# tác dụng: thêm log cho tất cả trang web ở trạng thái chờ(WAITING)
def set_all_website_waiting():
    # lấy ra thông tin của tất cả website
    websites = ConfigController.findAll(f'{API.get_context_config()}/findAll')
    # tạo json dateDim
    dateDimJson = {
        "fullDate": general.get_local_date()
    }

    # lấy ra id của dateDim hôm nay
    dateSk = DateDimController.getIdToday(f"{API.get_context_dateDim()}/id", dateDimJson)

    # lặp qua từng website
    for website in websites:
        # lấy ra tất cả id của website
        website_id = website["id"]
        print(website_id)
        # tạo json log
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
            "timeStart": general.get_local_date(),
            'dateSk': {
                'dateSk': dateSk
            }
        }
        # thêm log ở trạng thái WAITINg
        LogController.add(f"{API.get_context_log()}/add", logJson)


# tác dụng: gửi email thông báo tất cả trang web đã sẵn sàng để lấy dữ liệu
def send_email_for_prepare(subject, message):
    res = EmailController.send(f'{API.get_context_email()}/send', API.get_receiver_email(), subject, message)
    return res


