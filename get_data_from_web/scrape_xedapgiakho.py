# ĐÂY LÀ LỚP CHÍNH ĐỂ LẤY DỮ LIỆU TỪ TRANG WEB XEDAPGIAKHO

import time
from selenium.webdriver.common.by import By
import pandas as pd
import API
import general
from controller.control import logController, statusController
from controller.control import controlController
from controller.staging import bikeController

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
    pages.append(item.get_attribute("href"))

  driver.quit()
  return pages

# tham số: đường dẫn của loại xe đạp
# tác dụng: lấy ra số lượng trang
# return: số trang
def get_quantity_page(page):
  driver = general.config()
  driver.get(page)
  i = 2
  result = []
  while True:
    url_page_number = page + f"/page/{i}/"
    driver.get(url_page_number)
    products = driver.find_elements(By.CLASS_NAME, 'products')
    result += products
    if len(products) == 0:
      break
    i += 1
  driver.quit()
  return len(result)

# tham số: danh sách đường dẫn của các loại xe đạp khác nhau
# tác dụng: lặp qua từng trang và lấy ra href của từng sản phẩm trong từng loại
# return: danh sách href của tất cả các sản phẩm trong từng loại
def get_link_xedapgiakho(pages):
  driver = general.config()
  hrefs = []

  for page in pages:
    quantity_page = get_quantity_page(page) + 1
    for i in range(1, quantity_page + 1):
      url_page_number = page + f"/page/{i}"
      driver.get(url_page_number)
      urls = driver.find_elements(By.CLASS_NAME, 'woocommerce-loop-product__link')
      for url in urls:
        href = url.get_attribute("href")
        hrefs.append(href)

  driver.quit()
  return hrefs

# tham số: danh sách href của tất cả các sản phẩm trong từng loại
# tác dụng: đi vào từng href và lấy về các thông tin như name, price, price_sale, ...
# return: danh sách từng sản phẩm, lưu bằng DataFrame
def get_data_detail_xedapgiakho(hrefs):
  print(hrefs)
  timeStartScrape = general.get_local_date_time()
  driver = general.config()

  data = pd.DataFrame(
    columns=['id', 'name', 'price', 'priceSale', 'brand', 'color', 'size', 'status', 'timeStartScrape',
             'timeEndScrape'])

  try:
    for href in hrefs:
      driver.get(href)
      name = driver.find_element(By.CLASS_NAME, 'product-title').text

      div_price = driver.find_element(By.CLASS_NAME, 'price-on-sale')
      try:
        price = div_price.find_elements(By.CLASS_NAME, 'woocommerce-Price-amount')[1].text
      except:
        price = ""

      size = ''
      brand = ''
      status = ''

      try:
        div_more = driver.find_element(By.CLASS_NAME, 'pum-trigger')
        div_more.find_element(By.CSS_SELECTOR, 'a').click()

        div_des = driver.find_element(By.CLASS_NAME, 'thong-so-ki-thuat-tab')
        time.sleep(5)
        rows = div_des.find_elements(By.CLASS_NAME, 'row-info')

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

      except:
        continue

      driver.quit()
      driver = general.config()
      driver.get('https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-vicky-crazy-vc600/')

      div_color = driver.find_elements(By.CLASS_NAME, 'isures-ivp--attr_item')
      print(len(div_color))
      i = 1
      try:
        for color in div_color:
          color.click()
          id = driver.find_element(By.CLASS_NAME, 'sku').text
          color_name = driver.find_element(By.CLASS_NAME, 'isures-ivp--selected').text

          try:
            price_sale = color.find_element(By.CLASS_NAME, 'woocommerce-Price-amount').text
            i += 1
          except:
            price_sale = ""

          timeEndScrape = general.get_local_date_time()
          bikeJson = {
            "id": id,
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
          bikeController.add(API.get_context_bike() + "/add", bikeJson)

          print("đang lấy dữ liệu...")
          data.loc[len(data)] = [id, name, price, price_sale, brand, color, size, status, timeStartScrape,
                                 timeEndScrape]
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
  # thêm log bắt đầu lấy dữ liệu------------------------------------------------------------------------------
  website = controlController.getIdByKeyword(f"{API.get_context_control()}/get", "xedapgiakho")
  id_website = website["id"]

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
    }
  }

  logController.add(f"{API.get_context_log()}/add", logJson)
  controlController.inscreaseScrapeTimes(f"{API.get_context_control()}/increase", id_website)

  # bắt đầu lấy dữ liệu------------------------------------------------------------------------------
  pages = get_page(url)
  hrefs = get_link_xedapgiakho(pages)
  data = get_data_detail_xedapgiakho(hrefs)
  # kết thúc lấy dữ liệu------------------------------------------------------------------------------

  # thêm log hoàn thành hoặc thất bại sau khi lấy xong dữ liệu-----------------------------------------
  timeEnd = general.get_local_date_time()
  if data.shape[0] > 0:
    # thêm log complete
    logJson['status'] = {
      "id": statusController.getStatusByName(f"{API.get_context_status()}/getStatusByName", API.get_type_complete())['id']
    }
    logJson["message"] = API.get_message("endMessage")
    logJson['timeEnd'] = timeEnd
    logJson['quantity'] = data.shape[0]
  else:
    # thêm log failed
    logJson['status'] = {
      "id": statusController.getStatusByName(f"{API.get_context_status()}/getStatusByName", API.get_type_failed())['id']
    }
    logJson["message"] = API.get_message("failedMessage")
    logJson['timeEnd'] = timeEnd

  logController.add(f"{API.get_context_log()}/add", logJson)

  # lưu file
  website = controlController.getIdByKeyword(f"{API.get_context_control()}/get", "xedapgiakho")
  save_folder = website["saveFolder"]
  general.to_excel(data, save_folder)

  return data


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
url = controlController.getIdByKeyword(f"{API.get_context_control()}/get", API.get_keyword_xedapgiakho())["website"]
data = general_xedapgiakho(url)

