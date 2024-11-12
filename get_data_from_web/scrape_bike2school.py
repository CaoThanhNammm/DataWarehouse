# ĐÂY LÀ LỚP CHÍNH ĐỂ LẤY DỮ LIỆU TỪ TRANG WEB BIKE2SCHOOL
import time

from selenium.webdriver.common.by import By
import pandas as pd
import API
import general
from controller.control import controlController, logController, statusController, dateDimController
from controller.staging import bikeController


# tham số: đường dẫn của trang web bike2school
# tác dụng: lấy ra đường dẫn các loại xe đạp khác nhau: xep đạp trẻ em, xe đạp thể thao, xe đạp đua
# return: danh sách đường dẫn của các loại xe đạp
def get_page_of_bike(url):
    driver = general.config()
    driver.get(url)

    container = driver.find_elements(By.CLASS_NAME, "container")

    type_of_bike = container[1].find_elements(By.CLASS_NAME, "top_categories_e")
    pages = []
    for type in type_of_bike:
        pages.append(type.get_attribute("href"))

    driver.quit()
    return pages

# tham số: danh sách đường dẫn của các loại xe đạp khác nhau
# tác dụng: lặp qua từng trang và lấy ra các đường dẫn của từng trang: như trang 1, trang 2, trang 3
# return: danh sách đường dẫn của từng trang của tất cả các loại xe đạp
def create_url_bike2school(pages, collection_num):
    i = 0
    urls = []

    for page in pages:
        driver = general.config()
        print(page)
        driver.get(page)

        try:
            num_pages = driver.find_elements(By.CLASS_NAME, "page-link")
            amount_page = int(num_pages[len(num_pages) - 2].text)

            for nums in range(1, amount_page + 1):
                urls.append(f'{page}?q=collections:{collection_num[i]}&page={nums}&view=grid')
        except:
            urls.append(page)

        i = i + 1
    return urls

# tham số: danh sách đường dẫn của từng trang của tất cả các loại xe đạp
# tác dụng: lặp qua từng trang và lấy ra các đường dẫn của từng sản phẩm
# return: danh sách đường dẫn của từng sản phẩm trong tất cả các trang
def get_hrefs_bike2school(urls):
    hrefs = []
    for url in urls:
        driver = general.config()
        print(url)
        driver.get(url)

        div_a = driver.find_elements(By.CLASS_NAME, 'news-item-products')
        for a in div_a:
            time.sleep(1)
            hrefs.append(a.find_element(By.CSS_SELECTOR, 'a').get_attribute("href"))
    return hrefs

# tham số: danh sách đường dẫn của từng sản phẩm trong tất cả các trang
# tác dụng: lặp qua từng sản phẩm và lấy ra các thông tin như name, price, ...
# return: danh sách từng sản phẩm, lưu bằng DataFrame
def get_data_detail_bike2school(hrefs):
    data = pd.DataFrame(
        columns=[
            'id', 'name', 'price', 'priceSale', 'brand', 'color', 'size', 'description', 'status', 'timeStartScrape', 'timeEndScrape'
        ])
    for href in hrefs:
        driver = general.config()
        driver.get(href)

        timeStartScrape = general.get_local_date_time()
        id = '-1'
        brand = 'N/A'
        color = 'N/A'
        size = 'N/A'
        time.sleep(1)
        try:
            div_des = driver.find_element(By.CLASS_NAME, "ba-text-fpt")
        except:
            div_des =  driver.find_element(By.CLASS_NAME, "fs-tsright")

        try:
            ul = div_des.find_element(By.XPATH, '/html/body/section[2]/div/div[1]/div/div[5]/div/div[2]/div[1]/div[1]/ul')
            description = ul.text
        except:
            description = ""

        try:
          name = driver.find_element(By.CLASS_NAME, 'title-head').text
        except:
          name = 'N/A'

        try:
            colors = driver.find_elements(By.CLASS_NAME, 'swatch-element.color')
            sizes = driver.find_elements(By.CLASS_NAME, 'swatch-element:not(.color)')
            print(len(colors), len(sizes))
            if colors and sizes:
                for color in colors:
                    color.click()
                    for size in sizes:
                        print("đang lấy dữ liệu...")
                        size.click()
                        status = driver.find_element(By.CLASS_NAME, 'a-stock').text
                        try:
                            price = driver.find_element(By.CLASS_NAME, 'product-price-old').text
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
                            "size": size.text,
                            "description_part1": description,
                            "timeStartScrape": timeStartScrape,
                            "timeEndScrape": timeEndScrape,
                            "status": status
                        }
                        data.loc[len(data)] = [id, name, price, price_sale, brand, color.text, size.text, description, status,
                                               timeStartScrape,
                                               timeEndScrape]
                        bikeController.add(API.get_context_bike() + "/add", bikeJson)
            elif colors:
                for color in colors:
                    color.click()
                    status = driver.find_element(By.CLASS_NAME, 'a-stock').text
                    try:
                        price = driver.find_element(By.CLASS_NAME, 'product-price-old').text
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
                        "description_part1": description,
                        "timeStartScrape": timeStartScrape,
                        "timeEndScrape": timeEndScrape,
                        "status": status
                    }
                    data.loc[len(data)] = [id, name, price, price_sale, brand, color.text, size, description, status,
                                           timeStartScrape,
                                           timeEndScrape]
                    bikeController.add(API.get_context_bike() + "/add", bikeJson)
            elif sizes:
                for size in sizes:
                    size.click()
                    status = driver.find_element(By.CLASS_NAME, 'a-stock').text
                    try:
                        price = driver.find_element(By.CLASS_NAME, 'product-price-old').text
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
                        "description_part1": description,
                        "timeStartScrape": timeStartScrape,
                        "timeEndScrape": timeEndScrape,
                        "status": status
                    }
                    data.loc[len(data)] = [id, name, price, price_sale, brand, color, size.text, description, status,
                                           timeStartScrape,
                                           timeEndScrape]
                    bikeController.add(API.get_context_bike() + "/add", bikeJson)
            else:
                status = driver.find_element(By.CLASS_NAME, 'a-stock').text
                try:
                    price = driver.find_element(By.CLASS_NAME, 'product-price-old').text
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
                    "description_part1": description,
                    "timeStartScrape": timeStartScrape,
                    "timeEndScrape": timeEndScrape,
                    "status": status
                }
                print("đang lấy dữ liệu...")
                data.loc[len(data)] = [id, name, price, price_sale, brand, color, size, description, status, timeStartScrape,
                                       timeEndScrape]
                bikeController.add(API.get_context_bike() + "/add", bikeJson)
        except:
            continue
    return data

# tham số: đường dẫn của trang web xedapgiakho
# tác dụng: phối hợp lại tất cả các method lại tạo ra 1 method hoàn chỉnh để lấy dữ liệu
# return: danh sách từng sản phẩm, lưu bằng DataFrame
def general_bike2school(url):
    # thêm log bắt đầu lấy dữ liệu------------------------------------------------------------------------------------
    website = controlController.getIdByKeyword(f"{API.get_context_control()}/get", API.get_keyword_bike2school())
    id_website = website["id"]

    # lấy ra id của datedim hôm nay
    dateDimJson = {
        "fullDate": general.get_local_date()
    }
    dateSk = dateDimController.getIdToday(f"{API.get_context_dateDim()}/id", dateDimJson)

    logJson = {
        "message": API.get_message("startMessage"),
        "quantity": 0,
        "timeStart": general.get_local_date_time(),
        "websiteId": {
            "id": id_website
        },
        'status': {
            "id":
                statusController.getStatusByName(f"{API.get_context_status()}/getStatusByName", API.get_type_running())["id"]
        },
        'dateSk': dateSk
    }

    logController.add(f"{API.get_context_log()}/add", logJson)
    controlController.inscreaseScrapeTimes(f"{API.get_context_control()}/increase", id_website)

    # bắt đầu lấy dữ liệu------------------------------------------------------------------------------
    collection_num = ['2432193', '2444695', '2444694', '', '2588496', '3221513', '2727345', '2719186', '3175753']

    # lấy ra từng trang của từng loại xe đạp
    pages = create_url_bike2school(get_page_of_bike(url),  collection_num)

    # lấy ra từng href của từng sản phẩm
    hrefs = get_hrefs_bike2school(pages)
    data = get_data_detail_bike2school(hrefs)

    website = controlController.getIdByKeyword(f"{API.get_context_control()}/get", API.get_keyword_bike2school())
    save_folder = website["saveFolder"]
    general.to_excel(data, save_folder)

    # kết thúc lấy dữ liệu------------------------------------------------------------------------------

    # thêm log hoàn thành hoặc thất bại sau khi lấy xong dữ liệu--------------------------------------------
    timeEnd = general.get_local_date_time()
    if data.shape[0] > 0:
        # thêm log complete
        logJson['status'] = {
            "id": statusController.getStatusByName(f"{API.get_context_status()}/getStatusByName", API.get_type_complete())['id']
        }
        logJson['timeEnd'] = timeEnd
        logJson['quantity'] = data.shape[0]
        logJson["message"] = API.get_message("endMessage")
    else:
        # thêm log failed
        logJson['status'] = {
            "id":
                statusController.getStatusByName(f"{API.get_context_status()}/getStatusByName", API.get_type_failed())['id']
        }
        logJson['timeEnd'] = timeEnd
        logJson["message"] = API.get_message("failedMessage")

    logController.add(f"{API.get_context_log()}/add", logJson)

    return data

# ---------------------------------------------------------------------------------------------------------------------------------------------
# url = "https://bike2school.vn"
# website = controlController.getIdByKeyword(f'{API.get_context_control()}/get', API.get_keyword_bike2school())['website']
# general_bike2school(url)

print({"fullDate": general.get_local_date()})
print(f"{API.get_context_dateDim()}/id")
print(dateDimController.getIdToday(f"{API.get_context_dateDim()}/id", {"fullDate": general.get_local_date()}))
