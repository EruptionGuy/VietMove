# VietMove – Smart Transit Planner  
**Bảng B2: Dự án sử dụng Python**

## 1. Giới thiệu

**VietMove** là ứng dụng Python hỗ trợ tìm lộ trình di chuyển tại **Hà Nội** bằng
giao thông công cộng, kết hợp việc việc so sánh với ô tô cá nhân.
Ứng dụng giúp người dùng:
- Tìm tuyến xe buýt, tàu điện phù hợp
- Ước lượng thời gian, chi phí
- Hiển thị lượng **CO₂ tiết kiệm được** khi dùng giao thông công cộng

Dự án hướng tới chủ đề **"Việt Nam vươn mình"** và phát triển bền vững.

## 2. Yêu cầu cài đặt

### 2.1. Phần mềm & nền tảng

- **Python:** phiên bản **3.10 trở lên**
- **Hệ điều hành:** Windows / macOS / Linux
- **Internet:** Bắt buộc (dùng bản đồ và định tuyến)

### 2.2. Thư viện Python sử dụng

- `customtkinter` – Giao diện người dùng
- `tkintermapview` – Hiển thị bản đồ
- `Pillow` – Xử lý hình ảnh
- `geopy` – Chuyển đổi địa chỉ ↔ tọa độ
- `requests` – Gọi API định tuyến

## 3. Cài đặt thư viện

Mở Terminal / Command Prompt, di chuyển đến thư mục dự án và chạy:

```bash
pip install customtkinter tkintermapview pillow geopy requests
````

## 4. Cấu trúc thư mục

```text
vietmove/
│
├── main.py          # File chính chạy ứng dụng
├── bus_routes.py    # Dữ liệu & thuật toán tìm tuyến xe buýt
├── theme.json       # Giao diện CustomTkinter
├── app-icon.png     # Biểu tượng ứng dụng
└── README.md        # Hướng dẫn sử dụng
```

## 5. Cách chạy chương trình

Tại thư mục chứa file `main.py`, chạy:

```bash
python main.py
```

Hoặc (macOS / Linux):

```bash
python3 main.py
```

Sau khi chạy, cửa sổ ứng dụng VietMove sẽ xuất hiện.

## 6. Hướng dẫn thao tác cơ bản

1. Nhập **điểm bắt đầu** vào ô “Bạn đang ở đâu?”
2. Nhập **điểm đến** vào ô “Bạn muốn đi đâu?”
3. Nhấn nút **“Tìm lộ trình”**
4. Ứng dụng sẽ hiển thị:

   * Tuyến xe buýt, tàu điện, ô tô phù hợp trên bản đồ
   * Đường đi bộ đến bến xe
   * ⏱️ Thời gian di chuyển ước tính
   * 💰 Giá vé
   * 🌱 Lượng CO₂ tiết kiệm được so với đi ô tô


## 7. Ý nghĩa và mục tiêu

VietMove giúp người dùng:

* Dễ tiếp cận giao thông công cộng
* Giảm phụ thuộc vào xe máy, ô tô cá nhân
* Giảm phát thải CO₂ và ô nhiễm không khí
* Góp phần xây dựng **đô thị xanh – giao thông bền vững** tại Việt Nam