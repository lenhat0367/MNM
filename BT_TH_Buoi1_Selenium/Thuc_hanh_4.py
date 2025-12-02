from builtins import range
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#khoi tao trinh duyet
driver = webdriver.Chrome()

for i in range(65, 91):
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22" + chr(i) + "%22"
    try:
        driver.get(url)
        
        # cho trang web tai xong
        time.sleep(3)
        
        #lay tat ca cac the ul
        ul_tags = driver.find_elements(By.TAG_NAME, "ul")
        print(len(ul_tags))
        
        ul_painter = ul_tags[20]
        
        #lay tat ca cac the li trong the ul
        li_tags = ul_painter.find_elements(By.TAG_NAME, "li")
        
        #tao danh sach cac url
        titles = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
        
        #in ra cac titles
        for title in titles:
            print(title)
    except:
        print("ERROR!")
driver.quit()
