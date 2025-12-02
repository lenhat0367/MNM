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
options = webdriver.firefox.options.Options();
options.binary_location ="C:/Program Files/Mozilla Firefox/firefox.exe"
# Thiết lập firefox chỉ hiện thị giao diện
options.headless = False

# Khởi tạo driver
driver = webdriver.Firefox(options = options, service=ser)

# Tạo url
url = 'https://gochek.vn/collections/micro-thu-am'

# Truy cập
driver.get(url)

# Tạm dừng khoảng 2 giây
time.sleep(1)
# 4. Trích xuất dữ liệu
products = driver.find_elements(By.CLASS_NAME, "pro-loop")
product_list = []

# Tao cac list
stt = []
ten_san_pham = []
gia_ban = []
hinh_anh = []

for product in products:
    try:
        # Tên sản phẩm
        name_element = product.find_element(By.CSS_SELECTOR, "h3.pro-name a")
        name = name_element.text.strip()
        
        # Giá sau khi giảm (Giá bán hiện tại)
        # Tìm span chứa giá bán hiện tại
        current_price_element = product.find_element(By.CSS_SELECTOR, ".pro-price.highlight span:not(.pro-price-del)")
        current_price = current_price_element.text.strip()
        
        # Giá trước khi giảm (Giá gốc)
        # Tìm thẻ <del> bên trong .pro-price-del
        original_price_element = product.find_element(By.CSS_SELECTOR, ".pro-price-del .compare-price")
        original_price = original_price_element.text.strip()

        # URL hình ảnh
        # Tìm thẻ <img> bên trong thẻ <picture>
        # Lấy thuộc tính 'src' hoặc 'data-src'. Ở đây, ta dùng 'src' cho hình ảnh chính (thường là hình đầu tiên)
        # Lưu ý: Các thẻ <source> có data-srcset, nhưng thẻ <img> cuối cùng có thuộc tính 'src' hoặc 'data-src' dễ lấy hơn.
        image_element = product.find_element(By.CSS_SELECTOR, "div.product-img img.img-loop")
        image_url = image_element.get_attribute("src")
        
        # Nếu src là rỗng hoặc không phải là URL hoàn chỉnh, thử lấy data-src
        if not image_url or "data:" in image_url:
            image_url = image_element.get_attribute("data-src")


        product_list.append({
            "Tên Sản Phẩm": name,
            "Giá Bán (Sau Giảm)": current_price,
            "Giá Gốc (Trước Giảm)": original_price,
            "URL Hình Ảnh": image_url
        })
        
    except Exception as e:
        # Bỏ qua nếu có lỗi khi trích xuất một sản phẩm (ví dụ: thiếu giá gốc)
        print(f"Lỗi khi xử lý sản phẩm: {e}. Bỏ qua.")
        continue

# Đóng trình điều khiển
driver.quit()

# 5. Lưu vào file XLSX
if product_list:
    df = pd.DataFrame(product_list)
    df.to_excel('danh_sach_sp_4.xlsx', index=False)
else:
    print("\n⚠️ Không tìm thấy sản phẩm nào để lưu.")