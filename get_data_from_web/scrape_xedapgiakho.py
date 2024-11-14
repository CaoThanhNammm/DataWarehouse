# ĐÂY LÀ LỚP CHÍNH ĐỂ LẤY DỮ LIỆU TỪ TRANG WEB XEDAPGIAKHO

import time
from selenium.webdriver.common.by import By
import pandas as pd
import API
import general
from controller.control import LogController, StatusController, DateDimController, ConfigController
from controller.staging import BikeController
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# tham số: đường dẫn của loại xe đạp
# tác dụng: lấy ra số lượng trang
# return: số trang
def get_quantity_page(page):
  driver = general.config()
  driver.get(page)
  i = 1
  result = []
  url_page_numbers = []
  while True:
    url_page_number = page + f"page/{i}/"
    driver.get(url_page_number)

    products = driver.find_elements(By.CLASS_NAME, 'products')
    # result += products
    if len(products) == 0:
      break

    url_page_numbers.append(url_page_number)
    print(url_page_number)
    i += 1
  driver.quit()
  return url_page_numbers

# tham số: danh sách đường dẫn của các loại xe đạp khác nhau
# tác dụng: lặp qua từng trang và lấy ra href của từng sản phẩm trong từng loại
# return: danh sách href của tất cả các sản phẩm trong từng loại
def get_link_xedapgiakho(pages):
  driver = general.config()
  hrefs = []

  for page in pages:
    # quantity_page = get_quantity_page(page) + 1
    url_page_numbers = get_quantity_page(page)
    for url_page_number in url_page_numbers:
      driver.get(url_page_number)
      urls = driver.find_elements(By.CLASS_NAME, 'woocommerce-loop-product__link')
      for url in urls:
        href = url.get_attribute("href")
        print(href)
        hrefs.append(href)

    # for i in range(1, quantity_page + 1):
    #   url_page_number = page + f"page/{i}/"
    #   driver.get(url_page_number)
    #   urls = driver.find_elements(By.CLASS_NAME, 'woocommerce-loop-product__link')
    #
    #   for url in urls:
    #     href = url.get_attribute("href")
    #     print(href)
    #     hrefs.append(href)

  driver.quit()
  return hrefs

# tham số: danh sách href của tất cả các sản phẩm trong từng loại
# tác dụng: đi vào từng href và lấy về các thông tin như name, price, price_sale, ...
# return: danh sách từng sản phẩm, lưu bằng DataFrame
def get_data_detail_xedapgiakho(hrefs):
  # hrefs = ['https://xedapgiakho.com/product/xe-dap-tre-em-be-trai-shukyo-k2-12-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-shukyo-s1-12-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-trai-shukyo-k2-14-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-trai-shukyo-k2-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-shukyo-s1-14-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-trai-shukyo-k2-18-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-trai-shukyo-k2-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-shukyo-s1-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-shukyo-s1-18-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-xaming-nu-2-giong-12-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-nam-xaming-baga-12-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-xaming-baga-14-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-xaming-nu-2-giong-14-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-melody-14-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-shukyo-s1-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-xaming-16-inch-khung-thep/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-xaming-nu-2-giong-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-xaming-xm06-18-inch-cao-cap/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-jsxiong-2301-hiphop-12-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-cho-be-gai-jsxiong-2304-12-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-hector-luna-12-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-trai-hector-polo-12-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-shukyo-s3-12-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-xaming-18-inch-xanh/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-18-inch-xaming-nu-mau-do/',
  #          'https://xedapgiakho.com/product/xe-dap-cho-be-gai-jsxiong-2304-14-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-jsxiong-2301-hiphop-14-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-melody-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-trai-melody-14-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-shukyo-s3-14-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-trai-melody-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-xaming-nu-2-giong-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-cho-be-gai-jsxiong-2305-12-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-cho-be-gai-jsxiong-2304-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-cho-be-trai-jsxiong-2301-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-shukyo-s3-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-cho-be-trai-jsxiong-2301-18-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-jsxiong-2304-18-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-trai-melody-18-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-shukyo-s3-18-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-cho-be-trai-jsxiong-2301-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-cho-be-gai-jsxiong-2305-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-hector-luna-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-trai-hector-polo-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-shukyo-s3-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-jsxiong-2304-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-borgki-225-12-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-borgki-kungfu-223-14-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-borgki-kungfu-223-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-borgki-225-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-trai-shukyo-k40-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-jsxiong-mini-18-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-borgki-kungfu-223-18-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-xaming-mini-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-gai-jsxiong-mini-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-toyou-ty-24-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-trai-shukyo-k40-18-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-tre-em-brave-will-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-trai-shukyo-k40-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-brave-will-b118/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-lanq-fd-43-12-inch-cao-cap/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-be-trai-jianer-j9-12-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-tre-em-borgki-18-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-20-brave-will-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-lanq-fd43-14-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-20-inch-to-you-ty-29/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-tre-em-borgki-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-tre-em-shukyo-k45-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royalbaby-jenny-12rbg4/',
  #          'https://xedapgiakho.com/product/royalbaby-little-swan-rb12-18-12-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-lanq-fd-43-cao-cap-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-fascino-120r-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-royal-baby-freestyle-fs7-12-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royalbaby-little-swan-14-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royalbaby-jenny-14-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royal-baby-freestyle-fs7-2/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-tre-em-brave-will-g20/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royalbaby-little-swan-16inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royalbaby-jenny-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royal-baby-freestyle-fs7-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-mtb-fornix-fn20-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royal-baby-flying-bear-rb16b/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-fornix-fx20-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royalbaby-little-swan/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royalbaby-jenny-18-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royal-baby-freestyle-fs7/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royalbaby-jenny-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royalbaby-galaxy-fleet-14-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royal-baby-mercury-16-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royal-baby-miamor/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-tre-em-miamor-jupiter/',
  #          'https://xedapgiakho.com/product/xe-dap-tre-em-royal-baby-miamor-20abr-20-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-tre-em-miamor-satum/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-fascino-fs126s-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-fascino-fs124s-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-vicky-crazy-vc600/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-vicky-crazy-vc800/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-califa-ck6-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-califa-ck4/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-califa-ql680/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-califa-cs500-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-gap-califa-cg20/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-brave-will-g24-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-brave-will-g26/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-fascino-323-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-fascino-328-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-califa-cr7/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-fascino-fr700s-phanh-dia-co/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-fascino-ft-700s/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-dtfly-b100-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-dtfly-b100-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-fornix-fr309/',
  #          'https://xedapgiakho.com/product/xe-dap-the-thao-thong-nhat-gn-20-pro/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-dtfly-b100-27-5-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-catani-ca-x6-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-catani-tr30/',
  #          'https://xedapgiakho.com/product/xe-dap-thong-nhat-mtb-26-05-ldh/',
  #          'https://xedapgiakho.com/product/xe-dap-banh-beo-califa-fat-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-fixed-gear-life-fix735-700c/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-kurashi-kon-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-kurashi-kon-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-fascino-558-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-papylus-pr700s-khung-nhom/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-papylus-pt700s-khung-nhom/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-thong-nhat-m26-01/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-calli-s1500/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-louis-shimano-toney/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-fascino-818-700c/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-dtfly-k-650-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-dtfly-k650-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-calli-r20/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-fascino-828-khung-nhom/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-trinx-tr216/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-catani-ca-2-1-700c/',
  #          'https://xedapgiakho.com/product/xe-dap-fixed-gear-brave-will-x-2/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-fascino-728-27-5-inch-khung-nhom-shimano-phanh-dia/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-catani-ca-pro-700c/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-26-inch-fornix-m5/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-kurashi-eagle-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-black-line-rs900/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-kurashi-suteki/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-trinx-tr218-27-5-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-dtfly-h-500-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-dtfly-sr7/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-life-mx1000-khung-nhom/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-satako-colona/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-life-rx50/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-dtfly-h-500-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-dtfly-r-024-700c/',
  #          'https://xedapgiakho.com/product/xe-dap-fixed-gear-life-horse-fx2/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-tx100/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-life-mx2000/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-catani-ca-28/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-califa-cr450/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-life-vic3-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-life-alberta-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-trinx-free-2-4/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-tx250/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-esplendor-1/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-life-hesky-27-5-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-fascino-triton/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-papylus-pr800/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-tx200/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-catani-ca-63/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-dtfly-sr80/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-giant-2021-atx-620-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-dtfly-x3-29-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-calli-r35-tay-de-lac-khung-nhom/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-tx28-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-dtfly-r5-khung-nhom-phanh-dia/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-dtfly-r-070a-tay-de-lac-700c/',
  #          'https://xedapgiakho.com/product/xe-dap-hybrid-life-hbr-xmas/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-life-vic5/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-life-mx3000/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-dtfly-x5-knight-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-fixed-gear-funky-locking-nhat-ban/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-tx300/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-life-lion-pro-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-life-toronto-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-calli-5900-27-5-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-catani-ca-62/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-papylus-pr900/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-momentum-ineed-street/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-giant-atx-610-2021-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-satako-fomater/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-tx500/',
  #          'https://xedapgiakho.com/product/xe-dap-the-thao-26-inch-giant-ineed-hunter-20/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-miamor-crush-cr-275/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-calli-6100/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-liv-meme-2-2023/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-life-reds-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-escape-3/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-tx600/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-life-light-700c/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-liv-alight-2/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-calli-r45/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-tx800/',
  #          'https://xedapgiakho.com/product/xe-dap-momentum-2021-ineed-espresso/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-liv-alight-3-dd-disc/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-rincon-2/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-giant-atx-720-2021-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-dtfly-r-2000/',
  #          'https://xedapgiakho.com/product/xe-dap-giant-liv-meme-1-2023-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-life-pathlite-700c/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-escape-3-disc/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-roam-4-disc/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-talon-4/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-life-mx7000/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-escape-2-2024/',
  #          'https://xedapgiakho.com/product/xe-dap-gap-folding-momentum-pakaway-1-2024/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-calli-r55/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-talon-2/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-roam-3-disc-2024/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-talon-3/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-twitter-leopard-pro/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-talon-3-29-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-calli-r65/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-escape-2-disc/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-escape-2-city-disc-2/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-roam-2-disc/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-life-rx550/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-twitter-r12/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-sava-ex7-r4700/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-dtfly-droop-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-twitter-r12/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-sava-ex7-st-r7000/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-twitter-r12-tay-ngang/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-satako-akita-29-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-nesto-tiger-29-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-sava-x7/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-escape-1-disc/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-sava-x9-r7000/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-twitter-r12-pro-rs24/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-nesto-fox/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-roam-1-disc/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-twitter-cyclone/',
  #          'https://xedapgiakho.com/product/twitter-cyclone-pro-2024/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-sava-x9-5-4700/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-dtfly-r3000/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-trinx-v1000-pro/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-sava-ex7/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-talon-0/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-2022-revolt-f1/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-sava-x98/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-twitter-r12-tiagra-r4700/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-fastroad-2-2024/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-sava-x9-2-r7000/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-tro-luc-dien-life-vision/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-nesto-leopard/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-nesto-ostrich/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-fastroad-advanced-2/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-adv-3-2024/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-twitter-r12-2/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-giant-tcr-advanced-2-pro/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-giant-liv-langma-advanced-2-qom/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-giant-tcr-advanced-1-pro/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-giant-tcr-advanced-0-pro/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-giant-propel-adv-pro-0-2024/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-giant-tcr-advanced-pro-0-di2/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-fascino-fs126s-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-fascino-fs124s-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-vicky-crazy-vc600/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-vicky-crazy-vc800/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-califa-ck6-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-califa-ck4/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-califa-ql680/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-califa-cs500-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-brave-will-g24-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-brave-will-g26/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-fascino-323-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-fascino-328-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-dtfly-b100-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-dtfly-b100-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-the-thao-thong-nhat-gn-20-pro/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-dtfly-b100-27-5-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-catani-ca-x6-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-thong-nhat-mtb-26-05-ldh/',
  #          'https://xedapgiakho.com/product/xe-dap-banh-beo-califa-fat-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-kurashi-kon-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-kurashi-kon-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-fascino-558-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-fascino-568-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-thong-nhat-m26-01/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-dtfly-k-650-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-dtfly-k650-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-trinx-tr216/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-fascino-728-27-5-inch-khung-nhom-shimano-phanh-dia/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-26-inch-fornix-m5/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-kurashi-eagle-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-black-line-rs900/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-trinx-tr218-27-5-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-dtfly-h-500-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-life-mx1000-khung-nhom/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-dtfly-h-500-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-life-mx2000/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-life-vic3-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-life-alberta-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-life-hesky-27-5-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-giant-2021-atx-620-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-dtfly-x3-29-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-tx28-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-life-vic5/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-life-mx3000/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-dtfly-x5-knight-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-life-lion-pro-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-life-toronto-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-calli-5900-27-5-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-giant-atx-610-2021-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-satako-fomater/',
  #          'https://xedapgiakho.com/product/xe-dap-the-thao-26-inch-giant-ineed-hunter-20/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-miamor-crush-cr-275/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-calli-6100/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-liv-meme-2-2023/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-life-reds-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-rincon-2/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-giant-atx-720-2021-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-giant-liv-meme-1-2023-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-roam-4-disc/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-talon-4/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-life-mx7000/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-talon-2/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-roam-3-disc-2024/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-talon-3/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-twitter-leopard-pro/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-talon-3-29-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-roam-2-disc/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-dtfly-droop-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-satako-akita-29-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-nesto-tiger-29-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-roam-1-disc/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-trinx-v1000-pro/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-talon-0/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-tro-luc-dien-life-vision/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-giant-adv-3-2024/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-fascino-ft-700s/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-fornix-fr309/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-catani-tr30/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-papylus-pt700s-khung-nhom/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-calli-s1500/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-louis-shimano-toney/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-fascino-818-700c/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-catani-ca-2-1-700c/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-catani-ca-pro-700c/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-mtb-dtfly-h-500-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-satako-colona/',
  #          'https://xedapgiakho.com/product/xe-dap-dia-hinh-dtfly-h-500-275-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-dtfly-r-024-700c/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-tx100/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-trinx-free-2-4/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-tx250/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-esplendor-1/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-tx200/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-catani-ca-63/',
  #          'https://xedapgiakho.com/product/xe-dap-hybrid-life-hbr-xmas/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-tx300/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-fly/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-momentum-ineed-street/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-tx500/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-escape-3/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-tx600/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-liv-alight-2/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-life-tx800/',
  #          'https://xedapgiakho.com/product/xe-dap-momentum-2021-ineed-espresso/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-liv-alight-3-dd-disc/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-escape-3-disc/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-escape-2-2024/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-escape-2-disc/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-escape-2-city-disc-2/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-twitter-r12/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-twitter-r12-tay-ngang/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-escape-1-disc/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-sava-x9-r7000/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-nesto-fox/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-2022-revolt-f1/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-fastroad-2-2024/',
  #          'https://xedapgiakho.com/product/xe-dap-touring-giant-fastroad-advanced-2/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-califa-cr7/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-fascino-fr700s-phanh-dia-co/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-papylus-pr700s-khung-nhom/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-calli-r20/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-fascino-828-khung-nhom/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-kurashi-suteki/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-dtfly-sr7/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-life-rx50/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-catani-ca-28/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-califa-cr450/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-fascino-triton/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-papylus-pr800/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-dtfly-sr80/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-calli-r35-tay-de-lac-khung-nhom/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-dtfly-r5-khung-nhom-phanh-dia/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-dtfly-r-070a-tay-de-lac-700c/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-catani-ca-62/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-papylus-pr900/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-life-light-700c/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-calli-r45/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-dtfly-r-2000/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-life-pathlite-700c/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-calli-r55/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-calli-r65/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-life-rx550/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-sava-ex7-r4700/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-twitter-r12/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-sava-ex7-st-r7000/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-sava-x7/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-twitter-r12-pro-rs24/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-twitter-cyclone/',
  #          'https://xedapgiakho.com/product/twitter-cyclone-pro-2024/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-sava-x9-5-4700/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-dtfly-r3000/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-sava-ex7/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-sava-x98/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-twitter-r12-tiagra-r4700/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-sava-x9-2-r7000/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-nesto-leopard/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-nesto-ostrich/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-twitter-r12-2/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-giant-tcr-advanced-2-pro/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-giant-liv-langma-advanced-2-qom/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-giant-tcr-advanced-1-pro/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-giant-tcr-advanced-0-pro/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-giant-propel-adv-pro-0-2024/',
  #          'https://xedapgiakho.com/product/xe-dap-dua-giant-tcr-advanced-pro-0-di2/',
  #          'https://xedapgiakho.com/product/xe-dap-pho-thong-tu-thien-inox/',
  #          'https://xedapgiakho.com/product/xe-dap-nu-xaming-mini-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-pho-thong-action-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-nu-dinhu-suon-1-ong/',
  #          'https://xedapgiakho.com/product/xe-dap-nu-brave-will-relax-2-suon-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-nu-brave-will-relax-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-duong-pho-fascino-fm26-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-duong-pho-city-fascino-fm24/',
  #          'https://xedapgiakho.com/product/xe-dap-nu-thong-nhat-new-24-2023/',
  #          'https://xedapgiakho.com/product/xe-dap-nu-swat-sw24b-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-nu-xaming-24g19-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-pho-thong-dtfly-26city-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-nu-califa-misa-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-mini-fascino-camellia-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-nu-brave-will-mini-q1-banh-26/',
  #          'https://xedapgiakho.com/product/xe-dap-nu-duong-pho-life-beauty-lb26/',
  #          'https://xedapgiakho.com/product/xe-dap-nu-duong-pho-miamor-honey/',
  #          'https://xedapgiakho.com/product/xe-dap-nu-pretty-latte-v-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-nu-duong-pho-miamor-honey-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-california-modeltime-cacao-26-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-duong-pho-touring-momentum-ineed-latte-26-2022/',
  #          'https://xedapgiakho.com/product/xe-dap-duong-pho-momentum-ineed-latte-26/',
  #          'https://xedapgiakho.com/product/giant-momentum-ineed-latte-2024-24-inch/',
  #          'https://xedapgiakho.com/product/xe-dap-nu-giant-momentum-ineed-latte-2023-26-inch/']
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

  # thêm log bắt đầu lấy dữ liệu------------------------------------------------------------------------------
  website = ConfigController.getIdByKeyword(f"{API.get_context_config()}/get", "xedapgiakho")
  id_website = website["id"]

  # lấy ra id của datedim hôm nay
  dateDimJson = {
    "fullDate": general.get_local_date()
  }
  dateSk = DateDimController.getIdToday(f"{API.get_context_dateDim()}/id", dateDimJson)

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
    # thêm log complete
    logJson['status'] = {
      "id": StatusController.getStatusByName(f"{API.get_context_status()}/getStatusByName", API.get_type_complete())['id']
    }
    logJson["message"] = API.get_message("endMessage")
    logJson['timeEnd'] = timeEnd
    logJson['quantity'] = data.shape[0]
  else:
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
