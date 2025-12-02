import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import re
import os # Thêm thư viện để kiểm tra/xóa file DB (tùy chọn)

######################################################
## I. Cấu hình và Chuẩn bị
######################################################

# Thiết lập tên file DB và Bảng
DB_FILE = 'Painters_Data.db'
TABLE_NAME = 'painters_info'
all_links = []

# Tùy chọn cho Chrome (có thể chạy ẩn nếu cần, nhưng để dễ debug thì không dùng)
# chrome_options = Options()
# chrome_options.add_argument("--headless") 

# Nếu muốn bắt đầu với DB trống, có thể xóa file cũ (Tùy chọn)
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"Đã xóa file DB cũ: {DB_FILE}")

# Mở kết nối SQLite và tạo bảng nếu chưa tồn tại
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Tạo bảng
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    name TEXT PRIMARY KEY, -- Sử dụng tên làm khóa chính để tránh trùng lặp
    birth TEXT,
    death TEXT,
    nationality TEXT
);
"""
cursor.execute(create_table_sql)
conn.commit()
print(f"Đã kết nối và chuẩn bị bảng '{TABLE_NAME}' trong '{DB_FILE}'.")

# Hàm đóng driver an toàn
def safe_quit_driver(driver):
    try:
        if driver:
            driver.quit()
    except:
        pass

######################################################
## II. Lấy Đường dẫn (URLs)
######################################################

print("\n--- Bắt đầu Lấy Đường dẫn ---")

# tai? noi chua link va tao datafarme rong
all_links = []
d = pd.DataFrame({
    'name': [], 'birth': [], 'death': [], 'nationality': []
})

for i in range(70, 71):
    driver = webdriver.Chrome()
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22" + chr(i) + "%22"
    try:
        # mo trang
        driver.get(url)
        
        # cho trang load
        time.sleep(2)
        
        # <<< PHẦN ĐIỀU CHỈNH QUAN TRỌNG NHẤT NẰM Ở ĐÂY >>>
        
        # 1. Lấy TẤT CẢ thẻ ul trong khu vực nội dung chính (id="mw-content-text")
        ul_tags_in_content = driver.find_elements(By.XPATH, '//*[@id="mw-content-text"]//ul')
        
        # 2. CHỌN thẻ ul THỨ HAI ([1]) - đây chính là danh sách họa sĩ
        ul_painters = ul_tags_in_content[1]
        
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")
        
        # 4. ĐẾM VÀ IN RA SỐ LƯỢNG
        so_luong_tac_gia = len(li_tags)
        print(f"✅ Trang {chr(i)}: Số lượng tác giả trong danh sách chính là: {so_luong_tac_gia}")
        # <<< KẾT THÚC ĐIỀU CHỈNH >>>
        
        # lay tat ca the li trong the ul
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")
        
        # tao danh sach chua link
        link = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
        for x in link:
            all_links.append(x)
            
    except IndexError:
        print(f"ERROR! Không tìm thấy đủ 2 thẻ <ul> trong nội dung chính của trang {chr(i)}.")
    except Exception as e:
        print(f"ERROR! Lỗi chung khi xử lý trang {chr(i)}: {e}")
    
    #dong trinh duyet
    driver.quit()

######################################################
## III. Lấy thông tin & LƯU TRỮ TỨC THỜI
######################################################

print("\n--- Bắt đầu Cào và Lưu Trữ Tức thời ---")
count = 0
for link in all_links:
    # Giới hạn số lượng truy cập để thử nghiệm nhanh
    if (count >= 5): # Đã tăng lên 5 họa sĩ để có thêm dữ liệu mẫu
        break
    count = count + 1

    driver = None
    try:
        # khoi tao trinh duyet
        driver = webdriver.Chrome()
        #mo trang
        url = link
        driver.get(url)
        time.sleep(2)  #cho trang load
        
        # Lay ten hoa si (Giữ nguyên)
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""

        # Lay ngay sinh (Không dùng re.findall)
        try:
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            birth = birth_element.text  # Giữ nguyên toàn bộ chuỗi text
        except:
            birth = ""

        # Lay ngay mat (Không dùng re.findall)
        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            death = death_element.text  # Giữ nguyên toàn bộ chuỗi text
        except:
            death = ""

        # Lay quoc tich (Giữ nguyên)
        try:
            nationality_element = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td")
            nationality = nationality_element.text
        except:
            nationality = ""

        safe_quit_driver(driver)
        
        # 5. LƯU TỨC THỜI VÀO SQLITE
        insert_sql = f"""
        INSERT OR IGNORE INTO {TABLE_NAME} (name, birth, death, nationality) 
        VALUES (?, ?, ?, ?);
        """
        # Sử dụng 'INSERT OR IGNORE' để bỏ qua nếu Tên (PRIMARY KEY) đã tồn tại
        cursor.execute(insert_sql, (name, birth, death, nationality))
        conn.commit()
        print(f"  --> Đã lưu thành công: {name}")

    except Exception as e:
        print(f"Lỗi khi xử lý hoặc lưu họa sĩ {link}: {e}")
        safe_quit_driver(driver)
        
print("\nHoàn tất quá trình cào và lưu dữ liệu tức thời.")

######################################################
## IV. Truy vấn SQL Mẫu và Đóng kết nối
######################################################

conn = sqlite3.connect(DB_FILE)
    
# Hàm chung để thực thi và in kết quả
def execute_and_print(title, sql_query):
    print(f"\n=======================================================")
    print(f"## {title}")
    print(f"SQL: {sql_query.strip()}")
    print("-------------------------------------------------------")
    
    # Đọc dữ liệu vào DataFrame để in ra định dạng dễ nhìn
    try:
        df = pd.read_sql_query(sql_query, conn)
        if not df.empty:
            print(df.to_string(index=False))
        else:
            print("Không tìm thấy kết quả phù hợp.")
    except Exception as e:
        print(f"Lỗi khi thực thi truy vấn: {e}")
        
# 1. Đếm tổng số họa sĩ
sql_1 = f"""
SELECT COUNT(name) AS TotalPainters FROM {TABLE_NAME};
"""
execute_and_print("1. Tổng số họa sĩ đã lưu trữ", sql_1)

# 2. Hiển thị 5 dòng dữ liệu đầu tiên
sql_2 = f"""
SELECT * FROM {TABLE_NAME} LIMIT 5;
"""
execute_and_print("2. 5 dòng dữ liệu đầu tiên", sql_2)

# 3. Liệt kê danh sách các quốc tịch duy nhất
sql_3 = f"""
SELECT DISTINCT nationality FROM {TABLE_NAME} 
WHERE nationality IS NOT NULL AND nationality != '' 
ORDER BY nationality;
"""
execute_and_print("3. Danh sách các quốc tịch duy nhất", sql_3)

# ======================================================
# B. Yêu Cầu Lọc và Tìm Kiếm
# ======================================================

# 4. Tên của các họa sĩ có tên bắt đầu bằng ký tự 'F'
sql_4 = f"""
SELECT name FROM {TABLE_NAME} WHERE name LIKE 'F%';
"""
execute_and_print("4. Họa sĩ có tên bắt đầu bằng 'F'", sql_4)

# 5. Họa sĩ có quốc tịch chứa từ khóa 'French'
sql_5 = f"""
SELECT name, nationality FROM {TABLE_NAME} 
WHERE nationality LIKE '%French%';
"""
execute_and_print("5. Họa sĩ có quốc tịch chứa 'French'", sql_5)

# 6. Họa sĩ không có thông tin quốc tịch
sql_6 = f"""
SELECT name FROM {TABLE_NAME} 
WHERE nationality IS NULL OR nationality = '';
"""
execute_and_print("6. Họa sĩ KHÔNG có thông tin quốc tịch", sql_6)

# 7. Họa sĩ có cả thông tin ngày sinh và ngày mất
sql_7 = f"""
SELECT name FROM {TABLE_NAME} 
WHERE (birth IS NOT NULL AND birth != '') 
AND (death IS NOT NULL AND death != '');
"""
execute_and_print("7. Họa sĩ có cả ngày sinh VÀ ngày mất", sql_7)

# 8. Tất cả thông tin của họa sĩ có tên chứa '%Fales%'
sql_8 = f"""
SELECT * FROM {TABLE_NAME} 
WHERE name LIKE '%Fales%';
"""
execute_and_print("8. Thông tin họa sĩ có tên chứa '%Fales%'", sql_8)

# ======================================================
# C. Yêu Cầu Nhóm và Sắp Xếp
# ======================================================

# 9. Sắp xếp và hiển thị tên theo thứ tự bảng chữ cái (A-Z)
sql_9 = f"""
SELECT name FROM {TABLE_NAME} ORDER BY name ASC;
"""
execute_and_print("9. Tên họa sĩ được sắp xếp (A-Z)", sql_9)

# 10. Nhóm và đếm số lượng họa sĩ theo từng quốc tịch
sql_10 = f"""
SELECT nationality, COUNT(name) AS total_painters 
FROM {TABLE_NAME} 
WHERE nationality IS NOT NULL AND nationality != '' 
GROUP BY nationality 
ORDER BY total_painters DESC, nationality ASC;
"""
execute_and_print("10. Thống kê số lượng họa sĩ theo Quốc tịch", sql_10)

print("\n-------------------------------------------------------")
print("Hoàn tất tất cả các truy vấn.")
"""
A. Yêu Cầu Thống Kê và Toàn Cục
1. Đếm tổng số họa sĩ đã được lưu trữ trong bảng.
2. Hiển thị 5 dòng dữ liệu đầu tiên để kiểm tra cấu trúc và nội dung bảng.
3. Liệt kê danh sách các quốc tịch duy nhất có trong tập dữ liệu.

B. Yêu Cầu Lọc và Tìm Kiếm
4. Tìm và hiển thị tên của các họa sĩ có tên bắt đầu bằng ký tự 'F'.
5. Tìm và hiển thị tên và quốc tịch của những họa sĩ có quốc tịch chứa từ khóa 'French' (ví dụ: French, French-American).
6. Hiển thị tên của các họa sĩ không có thông tin quốc tịch (hoặc để trống, hoặc NULL).
7. Tìm và hiển thị tên của những họa sĩ có cả thông tin ngày sinh và ngày mất (không rỗng).
8. Hiển thị tất cả thông tin của họa sĩ có tên chứa từ khóa '%Fales%' (ví dụ: George Fales Baker).

C. Yêu Cầu Nhóm và Sắp Xếp
9. Sắp xếp và hiển thị tên của tất cả họa sĩ theo thứ tự bảng chữ cái (A-Z).
10. Nhóm và đếm số lượng họa sĩ theo từng quốc tịch.
"""

# Đóng kết nối cuối cùng
conn.close()
print("\nĐã đóng kết nối cơ sở dữ liệu.")