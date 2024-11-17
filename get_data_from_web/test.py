
import time
from selenium.webdriver.common.by import By
import pandas as pd
import API
import general
from controller.control import LogController, StatusController, DateDimController, ConfigController, EmailController
from controller.staging import BikeController


driver = general.config()
driver.get('https://xedapgiakho.com/product/xe-dap-tre-em-xaming-16-inch-khung-thep/')

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
print(p1)
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

print('description_part1', description_part1)
print('description_part2', description_part2)
print('description_part3', description_part3)