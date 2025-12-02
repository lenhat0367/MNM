import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_universities_selenium():
    # 1. Khởi tạo trình duyệt
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Bỏ comment nếu muốn chạy ngầm (không hiện trình duyệt)
    
    print("🚀 Đang khởi động trình duyệt...")
    driver = webdriver.Chrome()
    
    try:
        # 2. Truy cập trang Wikipedia
        url = "https://en.wikipedia.org/wiki/List_of_universities_in_Vietnam"
        print(f"🔗 Đang truy cập: {url}")
        driver.get(url)
        
        # Đợi trang tải
        time.sleep(3)

        results = []

        # 3. Lấy tất cả các bảng dữ liệu
        tables = driver.find_elements(By.CSS_SELECTOR, "table.wikitable")
        print(f"📊 Tìm thấy {len(tables)} bảng dữ liệu. Đang trích xuất...")

        for table_idx, table in enumerate(tables):
            try:
                # --- A. XỬ LÝ HEADER ---
                # Lấy header của bảng để xác định vị trí cột
                headers = [th.text.strip().lower() for th in table.find_elements(By.CSS_SELECTOR, "tr:first-child th")]
                
                idx_eng = -1
                idx_vi = -1
                idx_abbr = -1

                # Tìm vị trí cột dựa trên từ khóa trong header
                for i, h in enumerate(headers):
                    if h in ['member', 'english name', 'school', 'university system', 'name']:
                        idx_eng = i
                    elif 'vietnamese' in h:
                        idx_vi = i
                    elif 'abbreviation' in h:
                        idx_abbr = i
                
                # Bỏ qua bảng nếu không tìm thấy cột Tên
                if idx_eng == -1 or idx_vi == -1:
                    continue

                # --- B. DUYỆT HÀNG DỮ LIỆU ---
                rows = table.find_elements(By.TAG_NAME, "tr")[1:]

                for row in rows:
                    # Lấy tất cả các ô (th và td) trong hàng
                    cells = row.find_elements(By.XPATH, "./*")
                    
                    # --- XỬ LÝ ROWSPAN (Ô BỊ GỘP) ---
                    # Tính toán độ lệch nếu hàng bị thiếu ô do rowspan (thường là cột Location)
                    current_idx_eng = idx_eng
                    current_idx_vi = idx_vi
                    current_idx_abbr = idx_abbr

                    if len(cells) < len(headers):
                        shift = len(headers) - len(cells)
                        current_idx_eng = max(0, idx_eng - shift)
                        current_idx_vi = max(0, idx_vi - shift)
                        current_idx_abbr = idx_abbr - shift if idx_abbr != -1 else -1

                    # --- TRÍCH XUẤT ---
                    try:
                        eng_name = cells[current_idx_eng].text.strip()
                        vi_name = cells[current_idx_vi].text.strip()
                        
                        abbr = ""
                        if current_idx_abbr != -1 and current_idx_abbr < len(cells):
                            abbr = cells[current_idx_abbr].text.strip()

                        if eng_name and vi_name:
                            results.append({
                                "Abbreviation": abbr,
                                "English Name": eng_name,
                                "Vietnamese Name": vi_name
                            })
                    except IndexError:
                        continue 

            except Exception as e:
                # print(f"Lỗi nhỏ ở bảng {table_idx}: {e}")
                continue

        return results

    finally:
        driver.quit()

# --- PHẦN LƯU FILE EXCEL ---
if __name__ == "__main__":
    data = get_universities_selenium()
    
    if data:
        # 1. Chuyển dữ liệu sang DataFrame của Pandas
        df = pd.DataFrame(data)
        
        # 2. Đặt tên file xuất ra
        excel_filename = "Danh_sach_Dai_hoc_Viet_Nam.xlsx"
        
        print(f"\n💾 Đang lưu {len(df)} dòng dữ liệu vào file '{excel_filename}'...")
        
        # 3. Xuất ra Excel
        # index=False: Để không ghi cột số thứ tự (0,1,2...) vào file Excel
        df.to_excel(excel_filename, index=False)
        
        print(f"🎉 THÀNH CÔNG! File đã được lưu tại thư mục hiện tại.")
        
        # In thử 5 dòng đầu ra màn hình để kiểm tra
        print("-" * 60)
        print("Dữ liệu mẫu:")
        print(df.head(5).to_string())
        print("-" * 60)
    else:
        print("Không tìm thấy dữ liệu nào để lưu.")