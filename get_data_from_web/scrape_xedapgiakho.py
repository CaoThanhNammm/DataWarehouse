# ĐÂY LÀ LỚP CHÍNH ĐỂ LẤY DỮ LIỆU TỪ TRANG WEB XEDAPGIAKHO

import time
from selenium.webdriver.common.by import By
import pandas as pd
import API
import general
from controller.control import LogController, StatusController, DateDimController, ConfigController, EmailController
from controller.staging import BikeController

# tham số: đường dẫn của trang web xedapgiakho
# tác dụng: lấy ra đường dẫn các loại xe đạp khác nhau: xep đạp trẻ em, xe đạp thể thao, xe đạp đua
# return: danh sách đường dẫn của các loại xe đạp
def get_page(url_home):
  driver = general.config()
  driver.get(url_home)
  pages = []

  main_menu = driver.find_element(By.ID, 'menu-main-menu-new')
  nav_top_link = main_menu.find_elements(By.CLASS_NAME, 'nav-top-link')[:6]
  for item in nav_top_link:
    page = item.get_attribute("href")
    print(page)
    pages.append(page)

  driver.quit()
  return pages

# tham số: đường dẫn của tất cả loại xe đạp
# tác dụng: lặp qua từng trang và lấy ra các đường dẫn của từng trang: như trang 1, trang 2, trang 3
# return: danh sách đường dẫn của từng trang của tất cả các loại xe đạp
def create_url_bike2school(page):
  driver = general.config()
  driver.get(page)
  i = 1
  urls= []
  while True:
    url = page + f"page/{i}/"
    driver.get(url)

    products = driver.find_elements(By.CLASS_NAME, 'products')
    if len(products) == 0:
      break

    urls.append(url)
    print(url)
    i += 1
  driver.quit()
  return urls

# tham số: danh sách đường dẫn của các loại xe đạp khác nhau
# tác dụng: lặp qua từng trang và lấy ra href của từng sản phẩm trong từng loại
# return: danh sách href của tất cả các sản phẩm trong từng loại
def get_link_xedapgiakho(pages):
  driver = general.config()
  hrefs = []

  for page in pages:
    url_page_numbers = create_url_bike2school(page)
    for url_page_number in url_page_numbers:
      driver.get(url_page_number)
      urls = driver.find_elements(By.CLASS_NAME, 'woocommerce-loop-product__link')
      for url in urls:
        href = url.get_attribute("href")
        print(href)
        hrefs.append(href)

  driver.quit()
  return hrefs

# tham số: danh sách href của tất cả các sản phẩm trong từng loại
# tác dụng: đi vào từng href và lấy về các thông tin như name, price, price_sale, ...
# return: danh sách từng sản phẩm, lưu bằng DataFrame
def get_data_detail_xedapgiakho(hrefs):
  driver = general.config()
  print(hrefs)
  timeStartScrape = general.get_local_date_time()

  data = pd.DataFrame(
    columns=['id', 'name', 'price', 'priceSale', 'brand', 'color', 'size', 'description_part1', 'description_part2',
             'description_part3', 'status', 'timeStartScrape', 'timeEndScrape'])

  try:
    for href in hrefs:
      driver.get(href)
      name = driver.find_element(By.CLASS_NAME, 'product-title').text

      div_price = driver.find_element(By.CLASS_NAME, 'price-on-sale')
      try:
        price = div_price.find_elements(By.CLASS_NAME, 'woocommerce-Price-amount')[1].text
      except:
        price = ""

      try:
        rows = driver.find_elements(By.CLASS_NAME, 'row-info')

        rows.pop(0)
        rows.pop(0)
        rows.pop(len(rows) - 1)

        description_part1 = ""
        description_part2 = ""
        description_part3 = ""

        p1, p2, p3 = general.split_array_into_three(rows)

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
        continue

      if description_part1 == "":
        description_part1 = 'N/A'

      if description_part2 == "":
        description_part2 = 'N/A'

      if description_part3 == "":
        description_part3 = 'N/A'

      size = 'N/A'
      brand = 'N/A'
      status = 'N/A'

      driver.get(href)
      div_color = driver.find_element(By.CLASS_NAME, 'isures-ivp--attribute_wrap')
      colors = div_color.find_elements(By.CLASS_NAME, 'isures-ivp--attr_item')
      print(len(colors))
      try:
        for color in colors:
          color.click()
          time.sleep(1)
          sku = driver.find_element(By.CLASS_NAME, 'sku').text
          color_name = driver.find_element(By.CLASS_NAME, 'isures-ivp--selected').text
          status = driver.find_element(By.CLASS_NAME, 'in-stock').text
          try:
            price_sale = color.find_element(By.CLASS_NAME, 'woocommerce-Price-amount').text
          except:
            price_sale = "N/A"

          timeEndScrape = general.get_local_date_time()
          bikeJson = {
            "id": sku,
            "name": name,
            "price": price,
            "priceSale": price_sale,
            "brand": brand,
            "color": color_name,
            "size": size,
            "description_part1": description_part1,
            "description_part2": description_part1,
            "description_part3": description_part3,
            "timeStartScrape": timeStartScrape,
            "timeEndScrape": timeEndScrape,
            "status": status
          }
          BikeController.add(API.get_context_bike() + "/add", bikeJson)

          print("đang lấy dữ liệu...")
          data.loc[len(data)] = [sku, name, price, price_sale, brand, color_name, size,
                                 description_part1, description_part2, description_part3,
                                 status, timeStartScrape, timeEndScrape]
      except Exception as e:
        print(e)
        continue
  except Exception as e:
    print(e)

  driver.quit()
  return data

# tham số: đường dẫn của trang web xedapgiakho
# tác dụng: phối hợp lại tất cả các method lại tạo ra 1 method hoàn chỉnh để lấy dữ liệu
# return: danh sách từng sản phẩm, lưu bằng DataFrame
def general_xedapgiakho(url):
  # lấy thông tin website------------------------------------------------------------------------------------
  website = ConfigController.getIdByKeyword(f"{API.get_context_config()}/get", "xedapgiakho")
  id_website = website["id"]

  # gửi email thông báo hệ thống đang chạy
  subject = API.get_subject_email()
  message = API.create_message_for_email(API.get_message_running()) + f": {website["website"]}"
  EmailController.send(f'{API.get_context_email()}/send', API.get_receiver_email(), subject, message)

  # lấy ra id của datedim hôm nay
  dateDimJson = {
    "fullDate": general.get_local_date()
  }
  dateSk = DateDimController.getIdToday(f"{API.get_context_dateDim()}/id", dateDimJson)
  # thêm log bắt đầu lấy dữ liệu
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
    'dateSk': {
      'dateSk': dateSk
    }
  }

  LogController.add(f"{API.get_context_log()}/add", logJson)
  ConfigController.inscreaseScrapeTimes(f"{API.get_context_config()}/increase", id_website)

  # bắt đầu lấy dữ liệu------------------------------------------------------------------------------
  pages = get_page(url)
  hrefs = get_link_xedapgiakho(pages)
  data = get_data_detail_xedapgiakho(hrefs)
  # kết thúc lấy dữ liệu------------------------------------------------------------------------------

  # thêm log hoàn thành hoặc thất bại sau khi lấy xong dữ liệu-----------------------------------------
  timeEnd = general.get_local_date_time()
  if data.shape[0] > 0:
    message = API.create_message_for_email(API.get_message_complete())+ f": {website["website"]}"
    EmailController.send(f'{API.get_context_email()}/send', API.get_receiver_email(), subject, message)

    # thêm log complete
    logJson['status'] = {
      "id": StatusController.getStatusByName(f"{API.get_context_status()}/getStatusByName", API.get_type_complete())['id']
    }
    logJson["message"] = API.get_message("endMessage")
    logJson['timeEnd'] = timeEnd
    logJson['quantity'] = data.shape[0]
  else:
    message = API.create_message_for_email(API.get_message_failed()) + f": {website["website"]}"
    EmailController.send(f'{API.get_context_email()}/send', API.get_receiver_email(), subject, message)

    # thêm log failed
    logJson['status'] = {
      "id": StatusController.getStatusByName(f"{API.get_context_status()}/getStatusByName", API.get_type_failed())['id']
    }
    logJson["message"] = API.get_message("failedMessage")
    logJson['timeEnd'] = timeEnd

  LogController.add(f"{API.get_context_log()}/add", logJson)

  # lưu file
  website = ConfigController.getIdByKeyword(f"{API.get_context_config()}/get", "xedapgiakho")
  save_folder = website["saveFolder"]
  general.to_excel(data, save_folder)

  return data


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
url = ConfigController.getIdByKeyword(f"{API.get_context_config()}/get", API.get_keyword_xedapgiakho())["website"]
data = general_xedapgiakho(url)
