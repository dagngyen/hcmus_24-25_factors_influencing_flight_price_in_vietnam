# **HCMUS - Intelligent Data Analysis Application**
Group 9: IntelHunter

Project: FLIGHT PRICE ANALYSIS (PHÂN TÍCH CÁC YẾU TỐ ẢNH HƯỞNG ĐẾN GIÁ VÉ MÁY BAY Ở VIỆT NAM)

Members:
- 20120524: Võ Đức Lợi
- 21120035: Nguyễn Hoài An
- 21120103: Phan Thảo Nguyên
- 21120179: Nguyễn Đặng Đăng Khoa
- 21120546: Nguyễn Thanh Sang

---

# **Hướng dẫn sử dụng**
## _Tổ chức không gian làm việc_
Trong github này được tổ chức như sau:
```css
📂official
 ┣ 📂data
 ┃ ┗ 📂daily_flight_data # Data sau khi crawl mỗi ngày sẽ được lưu bản sao .csv
 ┣ 📜ggflight_crawl.py # File main thực hiện chức năng crawl data
 ┣ 📜ggflight_dataframe.py # Định nghĩa các hàm bổ trợ
 ┣ 📜ggflight_selenium.py # Định nghĩa các hàm bổ trợ
 ┣ 📜ggflight_sql.py # Định nghĩa các hàm bổ trợ
 ┗ 📜requirements.txt # Phiên bản thư viện
📂temp # Nơi chứa rác đúng nghĩa và test code
📜README.md
```
Như vậy, từ dòng hướng dẫn này, ta coi folder `official` là thư mục làm việc chính và hướng dẫn dựa trên path của folder `official`.
## _Cài đặt phiên bản thư viện phù hợp_
Nếu quá trình thực thi code gặp một số vấn đề lỗi về phiên bản thư viện, hãy xem xét các thư viện cần thiết và tinh chỉnh phiên bản được đề cập trong `requirements.txt`:
```py
!pip install -r requirements.txt
```
## _Thực thi crawl dữ liệu_
```command
python ggflight_crawl.py
```

---

# **Khám phá dữ liệu**
Dữ liệu chính thức gồm các thuộc tính:
```command
- scrape_date (datetime): Ngày crawl dữ liệu
- id_departure (string): Sân bay đi
- id_arrival (string): Sân bay đến
- departure_datetime (datetime): Thời gian đi
- arrival_datetime (datetime): Thời gian đến
- airline (string): Hãng hàng không cung cấp dịch vụ
- travel_class (string): Hạng vé: Phổ thông và Thương gia
- is_nonstop (string): Số trạm dừng của chuyến bay
- price (float): Giá vé máy bay (đơn vị VND)
```