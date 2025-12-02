from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
import time
import pandas as pd

# Đường dẫn đến file thực thi geckodriver
gecko_path = r"D:/Cong viec/Ma_Nguon_Mo/BaiTap/geckodriver.exe"

# Khởi tởi đối tượng dịch vụ với đường geckodriver
ser = Service(gecko_path)

# Tạo tùy chọn
options = webdriver.firefox.options.Options()
options.binary_location ="C:/Program Files/Mozilla Firefox/firefox.exe"
# Thiết lập firefox chỉ hiện thị giao diện
options.headless = False

# Khởi tạo driver
driver = webdriver.Firefox(options = options, service=ser)

# Tạo url
url = 'https://luyencode.net/accounts/login/?next=/'

# Truy cập
driver.get(url)

# Tạm dừng khoảng 2 giây
time.sleep(2)

username_input = driver.find_element(By.XPATH, "//input[@name='username']")
password_input = driver.find_element(By.XPATH, "//input[@name='password']")

username_input.send_keys('lenhat0927')
time.sleep(1)
password_input.send_keys('Nhutcute3')

time.sleep(2)
buttton = driver.find_element(By.XPATH, "//button[@type='submit']")
buttton.click()
time.sleep(5)

driver.quit()