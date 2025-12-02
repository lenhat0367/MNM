from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# khoi tao web
driver = webdriver.Chrome()

# mo trang
url = "https://en.wikipedia.org/wiki/List_of_painters by name beginning with %22P%22"
driver.get(url)

time.sleep(3)  # cho trang web tai xong

#lay tat ca cac ca the ul
ul_tags = driver.find_elements(By.TAG_NAME, "ul")
print(len(ul_tags))

ul_painters = ul_tags[20]

li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
titles = [tag.find_element(By.TAG_NAME, "a").get_attribute("title") for tag in li_tags]

for link in links:
    print(link)

for title in titles:
    print(title)
    
driver.quit()