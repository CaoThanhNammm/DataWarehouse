# ĐÂY LÀ LỚP LẤY RA CÁC HẰNG SỐ LIÊN QUAN ĐẾN CHUNG CHUNG, CẤU HÌNH VÀ CÁC METHOD CHUNG

from selenium import webdriver
from datetime import datetime, date
import configparser

def config():
  options = webdriver.ChromeOptions()
  options.add_argument("--no-sandbox") # Tắt chế độ sandbox
  options.add_argument("--disable-dev-shm-usage") # Sử dụng bộ nhớ ảo
  return webdriver.Chrome(options=options)


def to_excel(data, file_name):
  data.to_excel(file_name, index=False)

def get_var_in_env(parent, child):
  config = configparser.ConfigParser()
  config.read('web.config')
  return config.get(parent, child)

def get_local_date_time():
  now = datetime.now()
  return now.isoformat()

def get_local_date():
  now =  date.today()
  return now.isoformat()

def split_array_into_three(arr):
    n = len(arr)

    part_size = n // 3
    remainder = n % 3

    # Chia mảng thành 3 phần
    part1 = arr[:part_size]
    part2 = arr[part_size:2 * part_size]
    part3 = arr[2 * part_size:]

    # Nếu có phần dư, phân phối nó cho các phần
    if remainder > 0:
        part1 += arr[2 * part_size]
    if remainder > 1:
        part2 += arr[2 * part_size + 1]

    return part1, part2, part3
