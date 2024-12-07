"""
    ĐÂY LÀ LỚP CHÍNH ĐỂ LẤY DỮ LIỆU TỪ TRANG WEB XEDAPGIAKHO
    Có 4 phương thức chính
    1. pages = get_page(url)
        - vào trang web lấy ra danh sách các loại
    2. hrefs = get_link_xedapgiakho(pages)
        - tạo ra danh sách url số trang, sau đó vào từng url số trang để lấy ra danh sách sản phẩm
    3. data = get_data_detail_xedapgiakho(hrefs)
         - vào từng sản phẩm để lấy ra thông tin
    4. general_xedapgiakho(url) tham số url là: https://xedapgiakho.com
        - kết hợp tất cả 1, 2, 3 lại thành 1 phương thức duy nhất
"""

import time
from selenium.webdriver.common.by import By
import pandas as pd
import API
import general
from controller.control import LogController, StatusController, DateDimController, ConfigController, EmailController
from controller.staging import BikeController


# tham số: url của trang web xedapgiakho: https://xedapgiakho.com
# tác dụng: lấy ra url các loại xe đạp khác nhau: xep đạp trẻ em, xe đạp thể thao, xe đạp đua
# return: danh sách url của các loại xe đạp
def get_page(url_home):
    driver = general.config()
    # vào trang chủ
    driver.get(url_home)
    pages = []

    # lấy ra div menu
    main_menu = driver.find_element(By.ID, 'menu-main-menu-new')
    # lấy ra tất cả thẻ a
    nav_top_link = main_menu.find_elements(By.CLASS_NAME, 'nav-top-link')[:6]
    # lặp qua từng thẻ a và lấy ra href
    for item in nav_top_link:
        page = item.get_attribute("href")
        print(page)
        pages.append(page)

    # tắt cấu hình
    driver.quit()
    return pages


# tham số: url của loại xe đạp
# tác dụng: lặp cho đến khi không tìm thấy sản phẩm(nghĩa là không còn trang nào)
# return: danh sách url của số trang
def create_url_bike2school(page):
    driver = general.config()
    # vào loại xe đạp
    driver.get(page)
    i = 1
    urls = []
    # lặp cho tới khi không tìm thấy sản phẩm
    while True:
        url = page + f"page/{i}/"
        driver.get(url)

        products = driver.find_elements(By.CLASS_NAME, 'products')
        # nếu kích thước sản phẩm bằng 0 thì không còn trang nào nữa
        if len(products) == 0:
            break
        urls.append(url)
        print(url)
        i += 1
    # tắt cấu hình
    driver.quit()
    return urls


# tham số: danh sách url của các loại xe đạp
# tác dụng: lặp qua từng loại xe đạp và lấy ra tất cả số trang. Sau đó lặp qua từng số trang để lấy ra danh sách url của chi tiết sản phẩm
# return: danh sách url của tất cả số trang
def get_link_xedapgiakho(pages):
    driver = general.config()
    hrefs = []

    # lặp qua từng loại
    for page in pages:
        # lấy ra danh sách url của tất cả số trang
        url_page_numbers = create_url_bike2school(page)

        # lặp qua từng url của tất cả số trang
        for url_page_number in url_page_numbers:
            # vào url của số trang
            driver.get(url_page_number)
            # lấy ra danh sách sản phẩm
            urls = driver.find_elements(By.CLASS_NAME, 'woocommerce-loop-product__link')
            # lặp qua từng sản phẩm và lấy ra url của chi tiết sản phẩm
            for url in urls:
                href = url.get_attribute("href")
                print(href)
                hrefs.append(href)

    # tắt cấu hình
    driver.quit()
    return hrefs


# tham số: danh sách url của tất cả sản phẩm
# tác dụng: lấy ra các thông tin như name, price, price_sale, ...
# return: danh sách từng sản phẩm, lưu bằng DataFrame
def get_data_detail_xedapgiakho(hrefs):
    quantity_product = len(hrefs)
    driver = general.config()
    print(hrefs)
    # lấy ra thời gian hiện tại
    timeStartScrape = general.get_local_date_time()

    # khởi tạo DataFrame có các cột cần lấy
    data = pd.DataFrame(
        columns=['id', 'name', 'price', 'priceSale', 'brand', 'color', 'size', 'description_part1', 'description_part2',
                 'description_part3', 'status', 'timeStartScrape', 'timeEndScrape'])
    i = 1
    # lặp qua từng sản phẩm
    for href in hrefs:
        # vào trang chi tiết sản phẩm
        driver.get(href)
        # lấy ra tên
        name = driver.find_element(By.CLASS_NAME, 'product-title').text
        time.sleep(1)
        # lấy ra div chứa giá giảm
        # lấy ra giá
        try:
            div_price = driver.find_element(By.CLASS_NAME, 'price-on-sale')
            price = div_price.find_elements(By.CLASS_NAME, 'woocommerce-Price-amount')[1].text
        except:
            price = ""

        try:
            # lấy ra danh sách chứa mô tả
            rows = driver.find_elements(By.CLASS_NAME, 'row-info')
            rows_info = []
            for row in rows:
                if row.text != "":
                    rows_info.append(row)


            description_part1 = ""
            description_part2 = ""
            description_part3 = ""

            # chia danh sách mô tả thành 3 phần bằng nhau
            p1, p2, p3 = general.split_array_into_three(rows_info)

            # lặp qua từng phần và lấy ra thông tin
            for row in p1:
                left = row.find_element(By.CLASS_NAME, 'left').text
                right = row.find_element(By.CLASS_NAME, 'right').text
                if left and right:
                    description_part1 += f"{left}: {right}"

            for row in p2:
                left = row.find_element(By.CLASS_NAME, 'left').text
                right = row.find_element(By.CLASS_NAME, 'right').text
                if left and right:
                    description_part2 += f"{left}: {right}"

            for row in p3:
                left = row.find_element(By.CLASS_NAME, 'left').text
                right = row.find_element(By.CLASS_NAME, 'right').text
                if left and right:
                    description_part3 += f"{left}: {right}"
        except Exception as e:
            description_part1, description_part2, description_part3 = "N/A", "N/A", "N/A"
            print("Lấy thông số kỹ thuật thất bại")
            print(e)

        size = 'N/A'
        brand = 'N/A'
        status = 'N/A'

        # vào lại trang chi tiết sản phẩm(do khi lấy mô tả trang web cần kéo xuống để lấy làm mất các element bên trên, nhưng mà các thông tin khác nằm bên trên)
        driver.get(href)
        time.sleep(1)
        try:
            # lấy ra div chứa danh sách color
            div_color = driver.find_element(By.CLASS_NAME, 'isures-ivp--attribute_wrap')
            # lấy ra danh sách color
            colors = div_color.find_elements(By.CLASS_NAME, 'isures-ivp--attr_item')

            print(len(colors))

            # lặp qua từng color
            for color in colors:
                # ấn vào color
                color.click()
                # đợi 1s để load
                time.sleep(1)
                # lấy ra id
                sku = driver.find_element(By.CLASS_NAME, 'sku').text
                # lấy ra màu được chọn
                color_name = driver.find_element(By.CLASS_NAME, 'isures-ivp--selected').text
                # lấy ra trạng thái
                status = driver.find_element(By.CLASS_NAME, 'in-stock').text
                # lấy ra giá giảm
                try:
                    price_sale = color.find_element(By.CLASS_NAME, 'woocommerce-Price-amount').text
                except:
                    price_sale = "N/A"
                # lấy ra thời gian hiện tại
                timeEndScrape = general.get_local_date_time()
                # tạo json bike
                bikeJson = {
                    "id": sku,
                    "name": name,
                    "price": price,
                    "priceSale": price_sale,
                    "brand": brand,
                    "color": color_name,
                    "size": size,
                    "description_part1": description_part1,
                    "description_part2": description_part2,
                    "description_part3": description_part3,
                    "timeStartScrape": timeStartScrape,
                    "timeEndScrape": timeEndScrape,
                    "status": status
                }
                # thêm vào CSDL
                BikeController.add(API.get_context_bike() + "/add", bikeJson)

                print("đang lấy dữ liệu...")
                # thêm vào DataFrame
                data.loc[len(data)] = [sku, name, price, price_sale, brand, color_name, size,
                                       description_part1, description_part2, description_part3,
                                       status, timeStartScrape, timeEndScrape]

            print(f'sản phẩm thứ {i}/{quantity_product}')
        except Exception as e:
            print(f'sản phẩm thứ {i}/{quantity_product} bị lỗi: {href}')
            print(e)

        i += 1
    # tắt cấu hình
    driver.quit()
    return data


# tham số: đường dẫn của trang web xedapgiakho: https://xedapgiakho.com
# tác dụng: phối hợp lại tất cả các method lại tạo ra 1 method hoàn chỉnh để lấy dữ liệu
# return: danh sách từng sản phẩm, lưu bằng DataFrame
def general_xedapgiakho(url):
    # lấy thông tin website------------------------------------------------------------------------------------
    website = ConfigController.getIdByKeyword(f"{API.get_context_config()}/get", API.get_keyword_xedapgiakho())
    # lấy ra id của website
    id_website = website["id"]

    # tạo chủ đề cho email
    subject = API.get_subject_email()
    # tạo nội dung cho email
    message = API.create_message_for_email(API.get_message_running()) + f": {website["website"]}"
    # gửi email thông báo hệ thống đang chạy
    EmailController.send(f'{API.get_context_email()}/send', API.get_receiver_email(), subject, message)

    # tạo json cho dateDim
    dateDimJson = {
        "fullDate": general.get_local_date()
    }
    # lấy ra id của datedim hôm nay
    dateSk = DateDimController.getIdToday(f"{API.get_context_dateDim()}/id", dateDimJson)

    # tạo json log
    logJson = {
        "message": API.get_message("startMessage"),
        "quantity": 0,
        "timeStart": general.get_local_date_time(),
        "websiteId": {
            "id": id_website
        },
        'status': {
            "id":
                StatusController.getStatusByName(f"{API.get_context_status()}/getStatusByName", API.get_type_running())[
                    "id"]
        },
        'dateSk': {
            'dateSk': dateSk
        }
    }
    # thêm log đang chạy(RUNNING)
    LogController.add(f"{API.get_context_log()}/add", logJson)
    # tăng số lần lấy dữ liệu lên 1
    ConfigController.inscreaseScrapeTimes(f"{API.get_context_config()}/increase", id_website)

    # bắt đầu lấy dữ liệu----------------------------------------------------------------------------------------------------
    # lấy ra danh sách url của tất cả loại xe đạp
    pages = get_page(url)
    # lấy ra danh sách url của tất cả sản phẩm
    hrefs = get_link_xedapgiakho(pages)
    # lấy ra danh sách thông tin của sản phẩm
    data = get_data_detail_xedapgiakho(hrefs)

    # lấy ra đường dẫn lưu file
    save_folder = f'{website["saveFolder"]}_{general.get_local_date()}.xlsx'
    # lưu file
    general.to_excel(data, save_folder)

    # kết thúc lấy dữ liệu--------------------------------------------------------------------------------------------

    # thêm log hoàn thành hoặc thất bại sau khi lấy xong dữ liệu----------------------------------------------------------
    timeEnd = general.get_local_date_time()

    # nếu số lượng lớn hơn 0 thì lấy thành công
    if data.shape[0] > 0:
        message = API.create_message_for_email(API.get_message_complete()) + f": {website["website"]}"
        EmailController.send(f'{API.get_context_email()}/send', API.get_receiver_email(), subject, message)

        # thêm log complete
        logJson['status'] = {
            "id": StatusController.getStatusByName(f"{API.get_context_status()}/getStatusByName",
                                                   API.get_type_complete())['id']
        }
        logJson["message"] = API.get_message("endMessage")
        logJson['timeEnd'] = timeEnd
        logJson['quantity'] = data.shape[0]
    else:
        # nếu số lượng bé hơn 0 thì lấy thất bại
        message = API.create_message_for_email(API.get_message_failed()) + f": {website["website"]}"
        EmailController.send(f'{API.get_context_email()}/send', API.get_receiver_email(), subject, message)

        # thêm log failed
        logJson['status'] = {
            "id":
                StatusController.getStatusByName(f"{API.get_context_status()}/getStatusByName", API.get_type_failed())[
                    'id']
        }
        logJson["message"] = API.get_message("failedMessage")
        logJson['timeEnd'] = timeEnd

    # lưu log thành công hoặc thất bại
    LogController.add(f"{API.get_context_log()}/add", logJson)
    return data


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# lấy url của website xepdapgiakho
url = ConfigController.getIdByKeyword(f"{API.get_context_config()}/get", API.get_keyword_xedapgiakho())["website"]
data = general_xedapgiakho(url)

