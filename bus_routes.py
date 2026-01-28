import math

# HELPER FUNCTIONS
def distance(a, b):
    """
    Calculate the approximate distance (in kilometers) between two GPS points a and b.
    """
    lat_km = 111
    lon_km = 111 * math.cos(math.radians((a[0] + b[0]) / 2))
    return math.sqrt(
        ((a[0] - b[0]) * lat_km) ** 2 +
        ((a[1] - b[1]) * lon_km) ** 2
    )

def near(point, coords, km=1):
    """
    Check all bus stops in coords. If at least one stop is within km kilometers of point, return True.
    """
    for c in coords:
      if distance(point, c) <= km:
          return True
    return False

# HANOI BUS ROUTE DATA (taken and reformatted from https://busmaps.com/en/vietnam/The-World-Bank/hanoi-gtfs)
BUS_ROUTES = [
  {
    "name": "Bus 01 – Yên Phụ – Long Biên – Gia Lâm",
    "price": "9.000đ",
    "coords": [
      [21.037449, 105.846857],  # Yên Phụ
      [21.033600, 105.847000],  # Quán Thánh
      [21.031316, 105.847041],  # Tôn Đức Thắng
      [21.026850, 105.847457],  # Hàng Bột
      [21.025799, 105.841261],  # Văn Miếu
      [21.019377, 105.837823],  # Ga Hà Nội
      [21.016060, 105.828116],  # Xã Đàn
      [21.011350, 105.825174],  # Đại La
      [21.010567, 105.824891],  # Bạch Mai
      [21.019183, 105.838374],  # Nguyễn Khoái
      [21.023583, 105.843891],  # Long Biên
      [21.035800, 105.857500],  # Ngọc Thụy
      [21.042300, 105.869100],  # Đức Giang
      [21.0482298, 105.8784425] # Bến xe Gia Lâm
    ]
  },

  {
    "name": "Bus 02 – Bưởi – Kim Mã – Giáp Bát",
    "price": "12.000đ",
    "coords": [
      [21.060200, 105.812800],  # Bưởi
      [21.048900, 105.820300],  # Thụy Khuê
      [21.041200, 105.819900],  # Kim Mã Thượng
      [21.033600, 105.814200],  # Giảng Võ
      [21.0295021, 105.8423455],# Điện Biên Phủ
      [21.022159, 105.848800],  # Lê Duẩn
      [21.016800, 105.841200],  # Giải Phóng
      [21.0049790, 105.8411961],# Bách Khoa
      [20.990400, 105.842700]   # Giáp Bát
    ]
  },

  {
    "name": "Bus 08 – Đông Anh – Long Biên – Hoàn Kiếm",
    "price": "9.000đ",
    "coords": [
      [21.091200, 105.806500],  # Đông Anh
      [21.075800, 105.825600],  # Bắc Thăng Long
      [21.056400, 105.842300],  # Nhật Tân
      [21.040900, 105.865100],  # Ngọc Thụy
      [21.035800, 105.857500],  # Long Biên
      [21.028866, 105.834708]   # Hoàn Kiếm
    ]
  },

  {
    "name": "Bus 12 – Hoàn Kiếm – Kim Mã – Hà Đông",
    "price": "12.000đ",
    "coords": [
      [21.028866, 105.834708],  # Hoàn Kiếm
      [21.033600, 105.814200],  # Kim Mã
      [21.026400, 105.808000],  # Giảng Võ
      [21.020500, 105.801100],  # Láng Hạ
      [21.012400, 105.790500],  # Khuất Duy Tiến
      [21.003200, 105.768800]   # Hà Đông
    ]
  },

  {
    "name": "Bus 18 – Xuân Thủy (ĐHQG) – Kim Mã – Hoàn Kiếm",
    "price": "12.000đ",
    "coords": [
      [21.038100, 105.782300],  # Xuân Thủy (ĐHQG)
      [21.033600, 105.814200],  # Kim Mã
      [21.0295021, 105.8423455],# Điện Biên Phủ
      [21.028866, 105.834708]   # Hoàn Kiếm
    ]
  },

  {
    "name": "Bus 20 – Gia Lâm – Long Biên – Cầu Giấy",
    "price": "12.000đ",
    "coords": [
      [21.0482298, 105.8784425], # Gia Lâm
      [21.035800, 105.857500],  # Long Biên
      [21.028866, 105.834708],  # Hoàn Kiếm
      [21.033600, 105.814200],  # Kim Mã
      [21.038100, 105.782300]   # Cầu Giấy
    ]
  },

  {
    "name": "Bus 30 – Linh Đàm – Hoàn Kiếm – Cầu Giấy",
    "price": "9.000đ",
    "coords": [
      [20.971800, 105.839700],  # Linh Đàm
      [21.0049790, 105.8411961],# Bách Khoa
      [21.019377, 105.837823],  # Ga Hà Nội
      [21.028866, 105.834708],  # Hoàn Kiếm
      [21.033600, 105.814200],  # Kim Mã
      [21.038100, 105.782300]   # Cầu Giấy
    ]
  },

  {
    "name": "Bus 38 – Nam Thăng Long – Kim Mã – Mai Động",
    "price": "12.000đ",
    "coords": [
      [21.060200, 105.812800],  # Nam Thăng Long
      [21.048900, 105.820300],  # Thụy Khuê
      [21.033600, 105.814200],  # Kim Mã
      [21.022159, 105.848800],  # Lê Duẩn
      [21.005167, 105.841360]   # Mai Động
    ]
  },

  {
    "name": "BRT 01 – Kim Mã – Yên Nghĩa",
    "price": "15.000đ",
    "coords": [
      [21.033600, 105.814200],  # Kim Mã
      [21.020500, 105.801100],  # Láng Hạ
      [21.012400, 105.790500],  # Khuất Duy Tiến
      [21.003200, 105.768800],  # Hà Đông
      [20.998200, 105.746600]   # Yên Nghĩa
    ]
  }

]

# FIND MATCHING BUS ROUTES
def find_matching_bus_routes(start, end):
    results = []

    # Direct routes
    for r in BUS_ROUTES:
        if near(start, r["coords"]) and near(end, r["coords"]): # If any station in a bus route is near your starting point and destination
            results.append({
                "type": "direct",
                "routes": [r],
            })

    if results:
        return results

    return results
