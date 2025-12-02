from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#tao 1 driver de bat dau
driver = webdriver.Chrome()

#mo trang web
driver.get("https://gomotungkinh.com/")
time.sleep(5)  #cho trang web tai xong

try:
    while True:
        driver.find_element(By.ID, "bonk").click()
        time.sleep(2)  #cho trang web kip cap nhat diem
except:
    driver.quit()