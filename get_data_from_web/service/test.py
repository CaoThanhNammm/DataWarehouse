from selenium.webdriver.common.by import By

import general

driver = general.config()
driver.get("https://bike2school.vn/xe-dap-the-thao-calli-1700")

colors = driver.find_elements(By.CLASS_NAME, 'swatch-element.color')
sizes = driver.find_elements(By.CLASS_NAME, 'swatch-element:not(.color)')
print(len(colors), len(sizes))
if colors and sizes:
    for color in colors:
        print(color.text)
        for size in sizes:
            print(size.text)
elif colors:
    print('asdsa')