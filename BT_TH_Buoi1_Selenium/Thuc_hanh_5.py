from pygments.formatters.html import webify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

#tao datafame chua thong tin can lay
d = pd.DataFrame({
    'name': [], 'birth': [], 'death': [], 'nationality': []
})

#khoi tao web
driver = webdriver.Chrome()

#mo trang
url = "https://en.wikipedia.org/wiki/Adolf_Hitler"
driver.get(url)

time.sleep(2)  #cho trang load

# Lay ten hoa si
try:
    name = driver.find_element(By.TAG_NAME, "h1").text
except:
    name = ""

# Lay ngay sinh
try:
    birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
    birth = birth_element.text
    birth = re.findall(r'[0-9]{1,2}[\s\.\-]+[A-Za-z]+\s+[0-9]{4}', birth)[0] 
except:
    birth = ""

# Lay ngay mat
try:
    death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
    death = death_element.text
    death = re.findall(r'[0-9]{1,2}[\s\.\-]+[A-Za-z]+\s+[0-9]{4}', death)[0]
except:
    death = ""

# Lay quoc tich
try:
    nationality_element = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td")
    nationality = nationality_element.text
except:
    nationality = ""
    
#tao dictionnary cua hoa sy
painter = {'name':name, 'birth':birth, 'death':death, 'nationality':nationality}

#chuyen thanh dataframe
painter_df = pd.DataFrame([painter])

#them thong tin
d = pd.concat([d, painter_df], ignore_index=True)

#in ra DF
print(d)

driver.quit()
