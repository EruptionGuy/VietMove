# VietMove – Smart Transit Planner  
**Bảng B2: Dự án sử dụng Python**

## 1. Giới thiệu dự án

**VietMove** là một ứng dụng Python hỗ trợ người dùng tra cứu lộ trình di chuyển
tại **Hà Nội** bằng các hình thức:
- 🚍 Xe buýt  
- 🚶‍♂️ Đi bộ  
- 🚗 Ô tô  

Dự án hướng tới chủ đề **“Việt Nam vươn mình”** và **phát triển bền vững**,
khuyến khích sử dụng giao thông công cộng thông qua việc hiển thị lượng **CO₂
có thể giảm được khi chọn xe buýt thay vì ô tô**.


## 2. Yêu cầu môi trường

- **Python:** phiên bản **3.10 trở lên**
- **Hệ điều hành:** Windows / macOS / Linux
- **Internet:** Bắt buộc (dùng bản đồ & định tuyến)


## 3. Thư viện sử dụng

Các thư viện ngoài được dùng trong dự án:

- `customtkinter`
- `tkintermapview`
- `Pillow`
- `geopy`
- `requests`


## 4. Cài đặt thư viện

Mở Terminal (hoặc Command Prompt), di chuyển đến thư mục dự án và chạy:

```bash
pip install customtkinter
pip install tkintermapview
pip install pillow
pip install geopy
pip install requests
```

Hoặc cài đặt tất cả cùng lúc:

```bash
pip install customtkinter tkintermapview pillow geopy requests
```


## 5. Cấu trúc thư mục

```text
vietmove/
│
├── main.py          # File chính chạy chương trình
├── bus_routes.py    # Dữ liệu & xử lý tuyến xe buýt
├── theme.json       # Giao diện CustomTkinter
├── app-icon.png     # Logo ứng dụng
└── README.md        # Hướng dẫn sử dụng
```


## 6. Cách chạy chương trình

Tại thư mục chứa `main.py`, chạy:

```bash
python main.py
```

Hoặc (macOS / Linux):

```bash
python3 main.py
```

## 7. Hướng dẫn sử dụng

1. Chọn **điểm xuất phát** và **điểm đến** từ danh sách.
2. Nhấn nút **“Tìm lộ trình”**.
3. Chọn tuyến xe buýt hoặc ô tô trong danh sách hiển thị.
4. Xem thông tin chi tiết:
   - ⏱️ Thời gian di chuyển  
   - ↔️ Khoảng cách  
   - 🌱 Lượng CO₂ phát thải / tiết kiệm  


## 8. Ý nghĩa dự án

VietMove góp phần:
- Khuyến khích sử dụng giao thông công cộng
- Giảm ùn tắc giao thông
- Giảm phát thải CO₂
- Hướng tới một **Việt Nam xanh và phát triển bền vững**