"""
    ĐÂY LÀ LỚP CHÍNH ĐỂ LẤY DỮ LIỆU TỪ TRANG WEB BIKE2SCHOOL
    Có 5 phương thức chính
    1. pages = get_page_of_bike(url)
        - vào trang web lấy ra danh sách các loại
    2. urls = create_url_bike2school(pages, collection_num)
        - vào từng loại để tạo ra danh sách tất cả số trang
    3. hrefs = get_hrefs_bike2school(urls)
        - vào từng số trang để lấy ra danh sách sản phẩm
    4. data = get_data_detail_bike2school(hrefs)
         - vào từng sản phẩm để lấy ra thông tin
    5. general_bike2school(url) tham số url là: https://bike2school.vn
        - kết hợp tất cả 1, 2, 3, 4 lại thành 1 phương thức duy nhất
"""
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import API
import general
from controller.control import ConfigController, LogController, StatusController, DateDimController, EmailController
from controller.staging import BikeController

# tham số: url của trang web bike2school
# tác dụng: lấy ra danh sách url các loại xe đạp khác nhau: xep đạp trẻ em, xe đạp thể thao, xe đạp đua
# return: danh sách url của các loại xe đạp
def get_page_of_bike(url):
    driver = general.config()
    # vào trang chủ
    driver.get(url)

    # lấy ra container chứa các loại của xe đạp
    container = driver.find_elements(By.CLASS_NAME, "container")
    time.sleep(1)
    type_of_bike = container[1].find_elements(By.CLASS_NAME, "top_categories_e")


    pages = []
    # lặp qua từng thẻ a, lấy ra href
    for type in type_of_bike:
        pages.append(type.get_attribute("href"))

    # tắt config sau khi lấy dữ liệu xong
    driver.quit()
    return pages

# tham số: danh sách url của các loại xe đạp, collection_num là mảng chứa các số theo như webiste cấu hình
# tác dụng: lặp qua từng loại và lấy ra các url của từng số trang như: trang 1, trang 2, trang 3
# return: danh sách url của tất cả số trang trong website
def create_url_bike2school(pages, collection_num):
    driver = general.config()
    i = 0
    urls = []
    # lặp qua các loại của xe đạp
    for page in pages:
        try:
            print(page)
            # vào từng loại xe đạp
            driver.get(page)

            try:
                # lấy ra các div là số trang bao gồm cả biểu tưởng "<<" và ">>"
                # nếu không có class page-link(nghĩa là chỉ có 1 trang) thì xử lý except
                num_pages = driver.find_elements(By.CLASS_NAME, "page-link")
                # để biết chính xác số trang là bnh phải trừ 2 biểu tượng  "<<" và ">>"
                amount_page = len(num_pages) - 2

                # lặp qua số lượng amount_page
                for nums in range(1, amount_page + 1):
                    # thêm vào url của từng số trang
                    urls.append(f'{page}?q=collections:{collection_num[i]}&page={nums}&view=grid')
            except:
                # nếu chỉ có 1 trang
                urls.append(page)

            i = i + 1
        except:
            # nếu bị mất config thì config lại để tiếp tục lấy dữ liệu
            driver = general.config()
            continue

    # tắt config sau khi lấy dữ liệu xong
    driver.quit()
    return urls

# tham số: danh sách url của tất cả số trang trong website
# tác dụng: lặp qua từng số trang và lấy ra các url của từng sản phẩm
# return: danh sách url của tất cả sản phẩm trong website
def get_hrefs_bike2school(urls):
    hrefs = []
    driver = general.config()

    # lặp qua từng số trang
    for url in urls:
        try:
            print(url)
            # vào số trang
            driver.get(url)

            # lấy ra div của tất sản phẩm trong trang đó
            div_a = driver.find_elements(By.CLASS_NAME, 'news-item-products')
            # lặp qua từng sản phẩm
            for a in div_a:
                # lấy ra thẻ a và href của thẻ a
                # thêm vào hrefs
                hrefs.append(a.find_element(By.CSS_SELECTOR, 'a').get_attribute("href"))
        except:
            # nếu bị mất config thì config lại để tiếp tục lấy dữ liệu
            driver = general.config()
            continue

    # tắt config sau khi lấy dữ liệu xong
    driver.quit()
    return hrefs

# tham số: danh sách url của tất cả sản phẩm trong website
# tác dụng: lặp qua từng sản phẩm và lấy ra các thông tin như name, price, ...
# return: danh sách thông tin của tất sản phẩm, lưu bằng DataFrame
def get_data_detail_bike2school(hrefs):
    driver = general.config()
    quantity_product = len(hrefs)

    # khởi tạo DataFrame có các cột cần lấy
    data = pd.DataFrame(
        columns=[
            'id', 'name', 'price', 'priceSale', 'brand', 'color', 'size', 'description_part1', 'description_part2', 'description_part3', 'status', 'timeStartScrape', 'timeEndScrape'
        ])

    i = 1
    # lặp qua từng sản phẩm
    for href in hrefs:
        # vào trang sản phẩm(là trang chi tiết sản phẩm)
        driver.get(href)

        # lấy ra thời gian hiện tại
        timeStartScrape = general.get_local_date_time()

        # khởi tạo biến lưu trữ thông tin
        id = 'N/A'
        brand = 'N/A'
        color = 'N/A'
        size = 'N/A'

        # lấy ra div chứa phần description(có thể ở 2 class "ba-text-fpt" hoặc "fs-tsright")
        try:
            div_des =  driver.find_element(By.CLASS_NAME, "fs-tsright")
        except:
            div_des = driver.find_element(By.CLASS_NAME, "ba-text-fpt")

        try:
            # lấy ra ul chứa các description(nếu không tìm thấy ul thì sẽ xử lý except)
            ul = div_des.find_element(By.CSS_SELECTOR, 'ul')

            # lấy ra tất cả thẻ li chứa từng mô tả chi tiết
            description = ul.find_elements(By.CSS_SELECTOR, 'li')

            infos = []
            for info in description:
                infos.append(info.text)

            # chia thành 3 phần bằng nhau vì quá dài
            description_part1, description_part2, description_part3 = general.split_array_into_three(infos)
            description_part1, description_part2, description_part3 = ' '.join(description_part1), ''.join(
                description_part2), ''.join(description_part3)
        except Exception as e:
            print(e)
            description_part1, description_part2, description_part3 = "N/A", "N/A", "N/A"

        try:
            # lấy ra tên sản phẩm
            name = driver.find_element(By.CLASS_NAME, 'title-head').text
        except:
            name = 'N/A'

        try:
            # lấy ra div chứa color
            colors = driver.find_elements(By.CLASS_NAME, 'swatch-element.color')
            # lấy ra div chứa size
            sizes = driver.find_elements(By.CLASS_NAME, 'swatch-element:not(.color)')

            """
                Trang web này có 4 trường hợp xảy ra cho mỗi chi tiết sản phẩm
                TH1. có color và size
                TH2. có color và không size
                TH3. có size và không color
                TH4. không color và size
            """

            # TH1
            if colors and sizes:
                # lặp qua từng color
                for color in colors:
                    # ấn vào color
                    color.click()
                    # lặp qua size
                    for size in sizes:
                        print("đang lấy dữ liệu...")
                        # ấn vào size
                        size.click()

                        # lấy ra trạng thái
                        status = driver.find_element(By.CLASS_NAME, 'a-stock').text

                        # lấy ra giá
                        try:
                            price = driver.find_element(By.CLASS_NAME, 'product-price-old').text
                            if price == "":
                                price = 'N/A'
                        except:
                            price = 'N/A'
                        # lấy ra giá giảm
                        try:
                            price_sale = driver.find_element(By.CLASS_NAME, 'product-price').text
                        except:
                            price_sale = 'N/A'

                        # lấy ra thời gian hiện tại
                        timeEndScrape = general.get_local_date_time()
                        # tạo json bike
                        bikeJson = {
                            "id": id,
                            "name": name,
                            "price": price,
                            "priceSale": price_sale,
                            "brand": brand,
                            "color": color.text,
                            "size": size.text,
                            "description_part1": description_part1,
                            "description_part2": description_part2,
                            "description_part3": description_part3,
                            "timeStartScrape": timeStartScrape,
                            "timeEndScrape": timeEndScrape,
                            "status": status
                        }

                        # thêm vào DataFrame
                        data.loc[len(data)] = [id, name, price, price_sale, brand, color.text, size.text,
                                               description_part1, description_part2, description_part3,
                                               status, timeStartScrape, timeEndScrape]

                        # thêm bike vào CSDL
                        BikeController.add(API.get_context_bike() + "/add", bikeJson)
            # TH2: giống bên trên nhưng k lặp qua size
            elif colors:
                for color in colors:
                    print("đang lấy dữ liệu...")
                    color.click()
                    status = driver.find_element(By.CLASS_NAME, 'a-stock').text
                    try:
                        price = driver.find_element(By.CLASS_NAME, 'product-price-old').text
                        if price == "":
                            price = 'N/A'
                    except:
                        price = 'N/A'

                    try:
                        price_sale = driver.find_element(By.CLASS_NAME, 'product-price').text
                    except:
                        price_sale = 'N/A'

                    timeEndScrape = general.get_local_date_time()
                    bikeJson = {
                        "id": id,
                        "name": name,
                        "price": price,
                        "priceSale": price_sale,
                        "brand": brand,
                        "color": color.text,
                        "size": size,
                        "description_part1": description_part1,
                        "description_part2": description_part2,
                        "description_part3": description_part3,
                        "timeStartScrape": timeStartScrape,
                        "timeEndScrape": timeEndScrape,
                        "status": status
                    }
                    data.loc[len(data)] = [id, name, price, price_sale, brand, color.text, size,
                                           description_part1, description_part2, description_part3,
                                           status, timeStartScrape, timeEndScrape]
                    BikeController.add(API.get_context_bike() + "/add", bikeJson)
            # TH3: giống bên trên nhưng k lặp qua color
            elif sizes:
                for size in sizes:
                    print("đang lấy dữ liệu...")
                    size.click()
                    status = driver.find_element(By.CLASS_NAME, 'a-stock').text
                    try:
                        price = driver.find_element(By.CLASS_NAME, 'product-price-old').text
                        if price == "":
                            price = 'N/A'
                    except:
                        price = 'N/A'

                    try:
                        price_sale = driver.find_element(By.CLASS_NAME, 'product-price').text
                    except:
                        price_sale = 'N/A'

                    timeEndScrape = general.get_local_date_time()
                    bikeJson = {
                        "id": id,
                        "name": name,
                        "price": price,
                        "priceSale": price_sale,
                        "brand": brand,
                        "color": color,
                        "size": size.text,
                        "description_part1": description_part1,
                        "description_part2": description_part2,
                        "description_part3": description_part3,
                        "timeStartScrape": timeStartScrape,
                        "timeEndScrape": timeEndScrape,
                        "status": status
                    }
                    data.loc[len(data)] = [id, name, price, price_sale, brand, color, size.text,
                                           description_part1, description_part2, description_part3,
                                           status, timeStartScrape, timeEndScrape]
                    BikeController.add(API.get_context_bike() + "/add", bikeJson)
            # TH4: giống bên trên nhưng k lặp qua cái nào hết
            else:
                print("đang lấy dữ liệu...")
                status = driver.find_element(By.CLASS_NAME, 'a-stock').text
                try:
                    price = driver.find_element(By.CLASS_NAME, 'product-price-old').text
                    if price == "":
                        price = 'N/A'
                except:
                    price = 'N/A'

                try:
                    price_sale = driver.find_element(By.CLASS_NAME, 'product-price').text
                except:
                    price_sale = 'N/A'

                timeEndScrape = general.get_local_date_time()
                bikeJson = {
                    "id": id,
                    "name": name,
                    "price": price,
                    "priceSale": price_sale,
                    "brand": brand,
                    "color": color,
                    "size": size,
                    "description_part1": description_part1,
                    "description_part2": description_part2,
                    "description_part3": description_part3,
                    "timeStartScrape": timeStartScrape,
                    "timeEndScrape": timeEndScrape,
                    "status": status
                }
                data.loc[len(data)] = [id, name, price, price_sale, brand, color, size,
                                       description_part1, description_part2, description_part3,
                                       status, timeStartScrape, timeEndScrape]
                BikeController.add(API.get_context_bike() + "/add", bikeJson)

            print(f'sản phẩm thứ {i}/{quantity_product}')
        except Exception as e:
            print(f'sản phẩm thứ {i}/{quantity_product} bị lỗi: {href}')
            print(e)

        i += 1
    # tắt cấu hình
    driver.quit()
    return data

# tham số: đường dẫn của trang web bike2school: https://bike2school.vn
# tác dụng: phối hợp lại tất cả các method lại tạo ra 1 method hoàn chỉnh để lấy dữ liệu
# return: danh sách từng sản phẩm, lưu bằng DataFrame
def general_bike2school(url):
    # lấy ra thông tin của website thông qua keyword------------------------------------------------------------------------------------
    website = ConfigController.getIdByKeyword(f"{API.get_context_config()}/get", API.get_keyword_bike2school())
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
                StatusController.getStatusByName(f"{API.get_context_status()}/getStatusByName", API.get_type_running())["id"]
        },
        'dateSk':{
            'dateSk': dateSk
        }
    }

    # thêm log đang chạy(RUNNING)
    LogController.add(f"{API.get_context_log()}/add", logJson)
    # tăng số lần lấy dữ liệu lên 1
    ConfigController.inscreaseScrapeTimes(f"{API.get_context_config()}/increase", id_website)

    # bắt đầu lấy dữ liệu------------------------------------------------------------------------------
    collection_num = ['2432193', '2444695', '2444694', '', '2588496', '3221513', '2727345', '2719186', '3175753']

    # lấy ra danh sách url của tất cả loại xe đạp
    pages = get_page_of_bike(url)
    # lấy ra danh sách url của tất cả số trang
    urls = create_url_bike2school(pages,  collection_num)
    # lấy ra url của tất cả sản phẩm
    hrefs = get_hrefs_bike2school(urls)
    # lấy ra tất cả thông tin của sản phẩm
    data = get_data_detail_bike2school(hrefs)

    # lấy ra đường dẫn lưu file
    save_folder = f'{website["saveFolder"]}_{general.get_local_date()}.xlsx'
    # lưu file
    general.to_excel(data, save_folder)

    # kết thúc lấy dữ liệu------------------------------------------------------------------------------

    # thêm log hoàn thành hoặc thất bại sau khi lấy xong dữ liệu--------------------------------------------
    timeEnd = general.get_local_date_time()

    # nếu số lượng lớn hơn 0 thì lấy thành công
    if data.shape[0] > 0:
        message = API.create_message_for_email(API.get_message_complete()) + f": {website["website"]}"
        EmailController.send(f'{API.get_context_email()}/send', API.get_receiver_email(), subject, message)

        # thêm log complete
        logJson['status'] = {
            "id": StatusController.getStatusByName(f"{API.get_context_status()}/getStatusByName", API.get_type_complete())['id']
        }
        logJson['timeEnd'] = timeEnd
        logJson['quantity'] = data.shape[0]
        logJson["message"] = API.get_message("endMessage")
    else:
        # nếu số lượng bé hơn 0 thì lấy thất bại
        message = API.create_message_for_email(API.get_message_failed() + f": {website["website"]}")
        EmailController.send(f'{API.get_context_email()}/send', API.get_receiver_email(), subject, message)

        # thêm log failed
        logJson['status'] = {
            "id":
                StatusController.getStatusByName(f"{API.get_context_status()}/getStatusByName", API.get_type_failed())['id']
        }
        logJson['timeEnd'] = timeEnd
        logJson["message"] = API.get_message("failedMessage")

    # lưu log thành công hoặc thất bại
    LogController.add(f"{API.get_context_log()}/add", logJson)
    return data

# ---------------------------------------------------------------------------------------------------------------------------------------------
# lấy url của website bike2schol
website = ConfigController.getIdByKeyword(f'{API.get_context_config()}/get', API.get_keyword_bike2school())['website']
general_bike2school(website)
