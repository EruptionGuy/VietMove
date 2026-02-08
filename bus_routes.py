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

BUS_AND_METRO_ROUTES = [
  {
    "name": "Bus 01 – Bến xe Gia Lâm - Bến xe Yên Nghĩa",
    "type": "bus",
    "price": "10.000đ",
    "coords": [
      [21.048372, 105.878294],  # Bến xe Gia Lâm
      [21.049693, 105.883499],  # 549 Nguyễn Văn Cừ
      [21.045525, 105.875224],  # 307 Nguyễn Văn Cừ
      [21.042326, 105.870461],  # 135 Nguyễn Văn Cừ
      [21.041333, 105.849344],  # E3.1 Điểm trung chuyển Long Biên
      [21.037591, 105.846962],  # 50 Hàng Cót
      [21.031037, 105.847072],  # 28 Đường Thành
      [21.026616, 105.847557],  # Bệnh viện Phụ sản TW
      [21.026171, 105.846400],  # Bệnh viện Phụ sản TW
      [21.025553, 105.841420],  # Tổng công ty Đường sắt Việt Nam
      [21.023782, 105.841347],  # Ga Hà Nội
      [21.019057, 105.837980],  # 46 Khâm Thiên
      [21.019346, 105.833606],  # 274-276 Khâm Thiên
      [21.015824, 105.828225],  # 142-144 Nguyễn Lương Bằng
      [21.011171, 105.825257],  # Gò Đống Đa - Tây Sơn
      [21.007133, 105.823130],  # 290 Tây Sơn
      [20.999645, 105.814802],  # Số 108 Nguyễn Trãi
      [20.993264, 105.806226],  # Chợ Thượng Đình, Nguyễn Trãi
      [20.995907, 105.809109],  # 322 Nguyễn Trãi
      [20.993462, 105.805676],  # 368 Nguyễn Trãi
      [20.990453, 105.801390],  # Bách hoá Thanh Xuân, Nguyễn Trãi
      [20.987770, 105.797642],  # 216 Nguyễn Trãi
      [20.985854, 105.794903],  # Công Ty CP Công Trình GT 873, Nguyễn Trãi
      [20.983411, 105.791632],  # 10 Trần Phú
      [20.980558, 105.787946],  # Học Viện Công Nghệ Bưu Chính Viễn Thông, Trần Phú (HĐ)
      [20.978563, 105.785560],  # Hồ Gươm Plaza, Trần Phú (HĐ)
      [20.975544, 105.781547],  # Khách sạn Sông Nhuệ
      [20.972566, 105.777512],  # Số 8 Quang Trung (HĐ)
      [20.970429, 105.774865],  # 80 Quang Trung (HĐ)
      [20.967539, 105.771240],  # 182 Quang Trung (HĐ)
      [20.963777, 105.766474],  # Quang Trung - Ga La Khê
      [20.961999, 105.764267],  # Giữa số 428 - 430 Quang Trung
      [20.959903, 105.761900],  # BRT Văn La
      [20.958272, 105.759239],  # 678 - 680 Quang Trung (HĐ)
      [20.953997, 105.753688],  # Nissan Hà Đông
      [20.952131, 105.751263],  # Đối Diện Trường TH Kinh Tế Hà Tây - Quốc Lộ 6
      [20.949967, 105.747722],  # Bến xe Yên Nghĩa
    ]
  },

  {
    "name": "Bus 02 – Bác Cổ - Bến xe Yên Nghĩa",
    "type": "bus",
    "price": "10.000đ",
    "coords": [
      [21.023586, 105.860681],  # Bác Cổ
      [21.022202, 105.861229],  # Trạm trung chuyển Trần Khánh Dư
      [21.018528, 105.860709],  # Đối diện Bệnh Viện Trung ương Quân đội 108 Trần Hưng Đạo
      [21.020498, 105.858321],  # Đại học Khoa học tự nhiên
      [21.023115, 105.857025],  # Vườn hoa 19-8 Hai Bà Trưng
      [21.024085, 105.853636],  # Tràng Tiền Plaza
      [21.024930, 105.850116],  # Bệnh viện Hữu Nghị Việt Nam - Cuba
      [21.026545, 105.849684],  # 6-8 Tràng Thi
      [21.029466, 105.846535],  # Bệnh viện Việt Đức
      [21.029311, 105.842339],  # Cửa Nam Điện Biên Phủ
      [21.031061, 105.839367],  # Vườn hoa Lênin Trần Phú
      [21.031058, 105.836118],  # Bệnh viện Xanh Pôn
      [21.028593, 105.834889],  # Văn Miếu Quốc Tử Giám
      [21.024859, 105.832736],  # Nhà thờ Hàng Bột
      [21.019988, 105.830444],  # Ngã 5 Ô Chợ Dừa
      [21.015944, 105.828287],  # 142-144 Nguyễn Lương Bằng
      [21.012061, 105.823925],  # Gò Đống Đa
      [21.007414, 105.82333],  # 290 Tây Sơn
      [20.999853, 105.81511],  # 108 Nguyễn Trãi
      [20.997752, 105.811959],  # Chợ Thượng Đình Nguyễn Trãi
      [20.995901, 105.809151],  # ĐH Khoa học - Tự nhiên Nguyễn Trãi
      [20.993488, 105.805671],  # Cục Sở hữu trí tuệ Nguyễn Trãi
      [20.99052, 105.801519],  # Bách hóa Thanh Xuân Nguyễn Trãi
      [20.987886, 105.797790],  # Đại học Hà Nội
      [20.985863, 105.794904],  # Công ty CP Công trình GT Nguyễn Trãi
      [20.983357, 105.791540],  # 10 Trần Phú Nguyễn Kim
      [20.980523, 105.788002],  # Học viện Bưu chính Viễn thông Trần Phú Hà Đông
      [20.975473, 105.781537],  # Đối diện Sở Tư pháp Hà Nội Trần Phú
      [20.972484, 105.777489],  # Bưu điện Hà Đông
      [20.970084, 105.774535],  # 80 Quang Trung Hà Đông
      [20.967582, 105.771339],  # Nhà thi đấu Hà Đông
      [20.963769, 105.766484],  # Ga La Khê 350-352 Quang Trung
      [20.962100, 105.764371],  # 428-430 Quang Trung
      [20.959962, 105.761603],  # BRT Văn La 530-532 Quang Trung
      [20.958115, 105.759239],  # 678-680 Quang Trung
      [20.954091, 105.75385],  # Nissan Hà Đông
      [20.949605, 105.747615],  # Bến xe Yên Nghĩa
    ]
  },

  {
    "name": "Bus 04 – Long Biên – Bệnh viện Nội tiết Trung ương Cơ sở 2",
    "type": "bus",
    "price": "10.000đ",
    "coords": [
      [21.041424, 105.849237],  # Điểm trung chuyển Long Biên (E3.4)
      [21.033314, 105.854407],  # Ngã 4 Nguyễn Hữu Huân - Hàng Mắm
      [21.028192, 105.855631],  # Cung thiếu Nhi Hà Nội
      [21.021503, 105.857838],  # Đối diện Đại học Dược Hà Nội
      [21.016498, 105.858488],  # 34-36 Tăng Bạt Hổ
      [21.014102, 105.859157],  # 48B Tăng Bạt Hổ
      [21.011484, 105.85914],  # 172 Lò Đúc
      [21.006789, 105.860837],  # 86 Kim Ngưu
      [21.002032, 105.861295],  # Tập thể E6 Quỳnh Mai
      [20.997758, 105.861759],  # Cửa hàng nhựa đường số 3 - 344 Kim Ngưu
      [20.995049, 105.862562],  # Đối diện 61 Tam Trinh
      [20.992212, 105.862906],  # Đối diện 161 - 163 Tam Trinh
      [20.990472, 105.864419],  # 20 Lĩnh Nam
      [20.964609, 105.820214],  # Đối diện 123 Lĩnh Nam
      [20.98413, 105.873945],  # Đối diện số 271 Lĩnh Nam
      [20.982847, 105.877349],  # Trường THPT Hoàng Văn Thụ, Lĩnh Nam
      [20.981191, 105.881506],  # 376-378 Lĩnh Nam
      [20.980079, 105.885669],  # Bưu Điện Trung Tâm 6 - 582 Lĩnh Nam
      [20.976768, 105.886151],  # Đình Nam Dư Hạ, Đỗ Mười
      [20.972918, 105.881157],  # Chùa Khuyến Lương, Đỗ Mười
      [20.965883, 105.875055],  # Số nhà 43 - Tổ 14 - Phường Yên Sở, Đỗ Mười
      [20.964523, 105.867652],  # Số nhà 30 Yên Sở, Phường Yên Sở, Đỗ Mười
      [20.965803, 105.852311],  # Đối diện Công Viên Yên Sở, Hoàng Mai, Đỗ Mười
      [20.966028, 105.844736],  # Qua lối rẽ khu hành chính quận Hoàng Mai, Đỗ Mười
      [20.964293, 105.841821],  # Đối diện bến xe Nước Ngầm, Ngọc Hồi
      [20.961212, 105.845037],  # Qua đối diện công Ty Cổ Phần Điện Công Nghiệp Hà Nội 30m, Ngõ 15 Ngọc Hồi
      [20.959643, 105.846079],  # Tòa nhà Nơ 3 - Trần Thủ Độ
      [20.955285, 105.846908],  # Nhà No9 KĐT Pháp Vân, Trần Thủ Độ
      [20.952464, 105.849827],  # BV Nội Tiết TW cơ sở 2
    ]
  },

  {
    "name": "Bus 11 – Công viên Thống Nhất - Học viện Nông nghiệp Việt Nam",
    "type": "bus",
    "price": "10.000",
    "coords": [
      [21.017162, 105.845215],  # CV Thống Nhất - Trần Nhân Tông
      [21.018203, 105.847430],  # 55 Quang Trung
      [21.021885, 105.848946],  # 67 Trần Hưng Đạo
      [21.023376, 105.857231],  # Nhà hát Lớn Hà Nội
      [21.026703, 105.856242],  # Ngân hàng Nhà nước Việt Nam - Vườn hoa Con Cóc
      [21.031985, 105.855717],  # 23 Hàng Tre - Ngã 4 Lò Sũ
      [21.034578, 105.854667],  # Hàng Muối - Cầu Chương Dương
      [21.037739, 105.852976],  # Đối diện Ô Quan Chưởng
      [21.042477, 105.865417],  # Chùa Ái Mộ
      [21.044629, 105.867705],  # 52 Ngọc Lâm
      [21.046195, 105.870726],  # 170 Ngọc Lâm
      [21.04903, 105.875875],  # Đối diện 447 Ngọc Lâm
      [21.052364, 105.886077],  # Phòng Công Chứng số 2 TPHN
      [21.053163, 105.889368],  # Cây xăng số 84 Cầu Chui (BĐX Gia Thụy)
      [21.049885, 105.891792],  # Đối diện Savico MegaMall Long Biên
      [21.046253, 105.894175],  # Đối diện Công ty nước sạch
      [21.038573, 105.898194],  # Đối diện UBND phường Phúc Đồng
      [21.031748, 105.909788],  # 523 Nguyễn Văn Linh - Khu CN Sài Đồng
      [21.029695, 105.914483],  # 693 Nguyễn Văn Linh - Ngã 3 Thạch Bàn
      [21.028113, 105.919992],  # Công ty May 10
      [21.023482, 105.931804],  # Ngã 3 cầu Thanh Trì - Nguyễn Đức Thuận
      [21.021517, 105.936463],  # Bưu cục Trâu Quỳ
      [21.018616, 105.936930],  # Ngã 3 Ngô Xuân Quảng - Nguyễn Mậu Tài
      [21.013244, 105.936057],  # Cửa hàng Xăng dầu số 100 - 234 Ngô Xuân Quảng
      [21.008846, 105.933909],  # Số 14 đường Học Viện Nông Nghiệp
      [21.004981, 105.932806],  # Học viện Nông Nghiệp Việt Nam
    ]
  },

  {
    "name": "Bus 12 – Công viên Nghĩa Đô - Khánh Hà (Thường Tín)",
    "type": "bus",
    "price": "10.000",
    "coords": [
      [21.037202, 105.801409],  # Đại học Thủ đô Hà Nội
      [21.035403, 105.803618],  # Cầu Dịch Vọng
      [21.031306, 105.802546],  # Đối diện Công viên Thủ Lệ - Đường Bưởi dưới
      [21.028536, 105.803845],  # Điểm trung chuyển Cầu Giấy - ĐHGTVT (cột sau)
      [21.026456, 105.803969],  # Tập thể điện tử Tàu Thủy, Huỳnh Thúc Kháng
      [21.021153, 105.804429],  # Đối diện Tòa án Nhân dân quận Đống Đa, Huỳnh Thúc Kháng
      [21.020548, 105.806905],  # Đối diện Tổng cục Khí tượng Thủy Văn, Huỳnh Thúc Kháng
      [21.01906, 105.80969],  # 57A Huỳnh Thúc Kháng
      [21.0171367, 105.81349],  # 7 Huỳnh Thúc Kháng
      [21.0157365, 105.815986],  # 171 Thái Hà
      [21.013119, 105.819701],  # 131 Thái Hà
      [21.010009, 105.822943],  # 3 Thái Hà - Bể bơi Thái Hà
      [21.008702, 105.825624],  # 251 Chùa Bộc
      [21.006413, 105.830449],  # 21 Chùa Bộc
      [21.002855, 105.82986],  # 20 Tôn Thất Tùng
      [20.999595, 105.828668],  # Trước tòa nhà Artemis
      [20.996125, 105.830057],  # 150 Lê Trọng Tấn
      [20.992829, 105.832108],  # Nhà công vụ QC PKKQ
      [20.989537, 105.830254],  # Đối diện siêu thị ACE Mart
      [20.986944, 105.832258],  # Công viên Định Công
      [20.984668, 105.833533],  # Đối diện Chợ xanh Định Công
      [20.984342, 105.840899],  # Đối diện 807 Giải Phóng
      [20.980426, 105.841239],  # Bến xe Giáp Bát
      [20.976232, 105.840634],  # Ga Giáp Bát - Giải Phóng
      [20.971689, 105.840763],  # Ngã 3 Giải Phóng - Linh Đàm
      [20.964293, 105.841821],  # Đối diện bến xe Nước Ngầm, Ngọc Hồi
      [20.960821, 105.841926],  # Trường PTTH Việt Nam Ba Lan, Ngọc Hồi
      [20.954963, 105.843247],  # Qua đường vào Bệnh viện đa khoa Thăng Long 60m, Ngọc Hồi
      [20.952095, 105.843848],  # Đối diện TCT Cơ điện Nông nghiệp & Thủy lợi, Ngọc Hồi
      [20.946601, 105.844216],  # Đối diện Trụ sở HĐND huyện Thanh Trì, Ngọc Hồi
      [20.942318, 105.843806],  # Qua ngã 3 Phan Trọng Tuệ, Ngọc Hồi
      [20.93881, 105.844378],  # Qua Khu tập thể LICÔLA 100m, Ngọc Hồi
      [20.935098, 105.845835],  # Gần ngã 3 đường Quỳnh Đô, Ngọc Hồi
      [20.932178, 105.846967],  # Qua Công ty CP Vận tải & Dịch vụ TS 15m, Ngọc Hồi
      [20.926844, 105.849359],  # Viện nghiên cứu Trồng & Phát triển Cây thuốc, Ngọc Hồi
      [20.924095, 105.848252],  # Chùa Ngọc Hồi
      [20.923056, 105.844731],  # Đối diện trường THCS Ngọc Hồi
    ]
  },

  {
    "name": "Bus 24 – Long Biên - Ngã Tư Sở - Cầu Giấy",
    "type": "bus",
    "price": "10.000đ",
    "coords": [
      [21.041222, 105.849512],  # Điểm trung chuyển Long Biên (E3.2)
      [21.032003, 105.856109],  # 162 Trần Quang Khải
      [21.025281, 105.859646],  # Vườn hoa Trần Quang Khải
      [21.022200, 105.861217],  # Trạm trung chuyển Trần Khánh Dư (Đảo đón khách)
      [21.017064, 105.862312],  # Đối diện K9 Bộ đội Biên phòng, Nguyễn Khoái
      [21.009705, 105.864842],  # Cạnh ngõ 18 Nguyễn Khoái
      [21.006354, 105.868041],  # Hè trước số nhà 202 - 204 Nguyễn Khoái
      [21.000797, 105.870575],  # 539 - 541 Minh Khai
      [20.998181, 105.866802],  # Imperia Garden 1
      [20.997098, 105.863895],  # 259 Minh Khai
      [20.995874, 105.860262],  # 199 Minh Khai
      [20.995626, 105.855029],  # 143 - 145 Minh Khai
      [20.996134, 105.850642],  # Số 5 Minh Khai (Chợ Mơ)
      [20.996437, 105.848040],  # 26 Đại La
      [20.997411, 105.843861],  # Tập thể A10 128C Đại La
      [20.998732, 105.838486],  # 86 Trường Chinh
      [21.000335, 105.831076],  # 184 Trường Chinh
      [21.002849, 105.821958],  # Platform dành riêng cho xe buýt trước nhà 610 Trường Chinh
      [21.003955, 105.818678],  # Platform dành riêng cho xe buýt trước nhà 80 Đường Láng
      [21.005917, 105.816719],  # Ga Láng - 220 Đường Láng
      [21.009864, 105.812859],  # 470 Đường Láng
      [21.013243, 105.807888],  # Chợ Láng Hạ A
      [21.01816, 105.803024],  # 794 Đường Láng
      [21.023409, 105.799316],  # 1014 Đường Láng
      [21.027244, 105.799495],  # 1178 Đường Láng
      [21.028525, 105.803852]  # Điểm trung chuyển Cầu Giấy - ĐHGTVT (cột sau)
    ]
  },

  {
    "name": "Bus 31 – Bách Khoa - Chèm",
    "type": "bus",
    "price": "10.000đ",
    "coords": [
      [21.006728, 105.845035],  # Đại học Bách Khoa
      [21.002739, 105.847565],  # Sân vận động Bách Khoa, Lê Thanh Nghị
      [21.006465, 105.847234],  # Đối diện B13 Ký túc xá Bách Khoa
      [21.010086, 105.85162],  # 319 Phố Huế
      [21.014307, 105.851777],  # 149 Phố Huế
      [21.018869, 105.851787],  # 25A-25B Phố Huế
      [21.021945, 105.854785],  # 25 Lý Thường Kiệt
      [21.023376, 105.857231],  # Nhà hát Lớn Hà Nội
      [21.026734, 105.856236],  # Ngân hàng Nhà nước Việt Nam - Vườn hoa con Cóc
      [21.031983, 105.855718],  # 23 Hàng Tre - Ngã 4 Lò Sũ
      [21.034579, 105.854672],  # Hàng Muối - Cầu Chương Dương
      [21.041380, 105.849584],  # Điểm trung chuyển Long Biên (E1.3)
      [21.044017, 105.847122],  # Dốc Hàng Than
      [21.046368, 105.844185],  # Nhà máy nước Yên Phụ
      [21.050158, 105.840795],  # Đường Yên Phụ - Bãi An Dương
      [21.053903, 105.837543],  # Chợ Yên Phụ
      [21.057112, 105.835697],  # Đền Bảo An, Nghi Tàm
      [21.059869, 105.833887],  # Số 34 Âu Cơ
      [21.063509, 105.831987],  # Số 132 Âu Cơ
      [21.066582, 105.827860],  # Số 236 Âu Cơ - Chợ hoa Quảng An
      [21.073701, 105.824889],  # Số 284 Âu Cơ - Hồ Quảng Bá
      [21.076067, 105.822214],  # Đối diện Đình Nhật Tân
      [21.080536, 105.818647],  # Ngã 3 Lạc Long Quân - Âu Cơ
      [21.084201, 105.816841],  # 8 An Dương Vương
      [21.090067, 105.811589],  # Đối diện Trạm thú y Tây Hồ 197 An Dương Vương
      [21.089865, 105.807772],  # Đối diện lối rẽ vào UBND phường Phú Thượng
      [21.089748, 105.802813],  # Đối diện 327 An Dương Vương
      [21.089407, 105.797047],  # Đối diện làng Thượng Thuỵ
      [21.090764, 105.788949],  # Xóm Đình Nhật Tảo (Cách đối diện Đình Nhật Tảo 100m)
      [21.092003, 105.782940],  # Đối diện trường tiểu học Đông Ngạc A
      [21.093611, 105.778608],  # Đối diện trường THCS Đông Ngạc A
      [21.090554, 105.777673],  # ĐD đình làng Liên Ngạc
      [21.082493, 105.778205],  # Đối diện Cửa hàng Bảo dưỡng sửa chữa xe máy Nam Hải Xóm 7 Đông Ngạc
      [21.025935, 105.988448],  # UBND phường Đức Thắng
      [21.073670, 105.777149],  # Trường CĐ Tài Nguyên & Môi Trường HN
      [21.071864, 105.777199]   # ĐH Mỏ
    ]
  },

  {
    "name": "Bus 38 – Tân Xuân – Mai Động",
    "type": "bus",
    "price": "12.000đ",
    "coords": [
      [21.087109, 105.785319],  # Tân Xuân
      [21.086798, 105.785282],  # Trường trung cấp nghề Thăng Long
      [21.074443, 105.785561],  # 138 Phạm Văn Đồng
      [21.062171, 105.7836],  # Trước 100m ngõ 218 Phạm Văn Đồng
      [21.058045, 105.782548],  # 370 Phạm Văn Đồng
      [21.05472, 105.781714],  # Siêu thị Metro Thăng Long
      [21.051546, 105.78132],  # Đối diện 36A Phạm Văn Đồng (Vincom Bắc Từ Liêm)
      [21.047687, 105.781089],  # Bộ Công An
      [21.046317, 105.784598],  # Trạm trung chuyển xe buýt Hoàng Quốc Việt (cột trước)
      [21.045991, 105.788393],  # Học viện Chính trị Quốc Gia Hồ Chí Minh
      [21.046018, 105.79216],  # Cao đẳng sư phạm mẫu giáo Trung ương
      [21.04599, 105.796282],  # 247-249 Hoàng Quốc Việt
      [21.039972, 105.797473],  # Công viên Nghĩa Đô
      [21.037200, 105.801417],  # Đại học Thủ đô Hà Nội
      [21.031306, 105.802546],  # Đối diện Công viên Thủ Lệ - Đường Bưởi dưới
      [21.028718, 105.803412],  # Điểm trung chuyển Cầu Giấy - ĐHGTVT (cột trước)
      [21.029397, 105.808861],  # 593 - 595 Kim Mã
      [21.028531, 105.821342],  # Trường THCS Giảng Võ
      [21.026872, 105.8243910],  # 113 Giảng Võ
      [21.032242, 105.829364],  # Hè trước tòa nhà PTA
      [21.031054, 105.833767],  # 145 Nguyễn Thái Học
      [21.029459, 105.838924],  # Trường Tiểu học Lý Thường Kiệt - Ngã 3 Hoàng Diệu
      [21.024047, 105.847852],  # 59 Lý Thường Kiệt
      [21.021962, 105.850346],  # 58B Bà Triệu
      [21.01917, 105.849429],  # 92-94 Bà Triệu
      [21.015878, 105.849126],  # 180 - 182 Bà Triệu
      [21.011365, 105.849028],  # Đối diện Vincom Tower
      [21.004035, 105.850973],  # 216-218 Bạch Mai
      [21.000201, 105.850439],  # 368-370 Bạch Mai
      [20.996803, 105.849984],  # 512-514 Bạch Mai
      [20.995702, 105.850684],  # 32 Minh Khai
      [20.995241, 105.854741],  # 218-220 Minh Khai
      [20.995666, 105.860883],  # 308 Minh Khai (Gần cầu Mai Động)
      [20.992268, 105.862365],  # Cách cổng Công ty cơ khí Trần Hưng Đạo 40m
      [20.987605, 105.863368],  # Đối diện 303 Nguyễn Tam Trinh
      [20.984938, 105.863657],  # Đối diện 411 Nguyễn Tam Trinh
      [20.980890, 105.863808],  # Bến xe Mai Động
    ]
  },

  {
    "name": "Bus 49 – Trần Khánh Dư - Nhổn",
    "type": "bus",
    "price": "10.000đ",
    "coords": [
      [21.022200, 105.861217],  # Trạm trung chuyển Trần Khánh Dư (Đảo đón khách)
      [21.018528, 105.860709],  # Đối diện Bệnh Viện Trung ương Quân đội 108 - Trần Hưng Đạo
      [21.020498, 105.858321],  # Đại học Khoa học tự nhiên
      [21.021995, 105.855276],  # 18 Lý Thường Kiệt
      [21.023037, 105.851743],  # Đối diện 39 Lý Thường Kiệt
      [21.023853, 105.848879],  # 44 Lý Thường Kiệt
      [21.024841, 105.845568],  # 54 Lý Thường Kiệt
      [21.023320, 105.841372],  # Ga Hà Nội
      [21.019022, 105.837981],  # 46 Khâm Thiên
      [21.01933, 105.834296],  # 274-276 Khâm Thiên
      [21.020354, 105.826835],  # Số 94 Ô Chợ Dừa
      [21.027720, 105.827682],  # Đối diện Ga Cát Linh - Hào Nam
      [21.028438, 105.825457],  # Bộ Y Tế
      [21.019788, 105.816509],  # Đối diện 251 Giảng Võ
      [21.023881, 105.816826],  # 666-668 Đê La Thành
      [21.027408, 105.809379],  # Ngõ 1072 Đê La Thành
      [21.029406, 105.803583],  # Điểm trung chuyển Cầu Giấy - Thủ Lệ (Cột trước)
      [21.033002, 105.798592],  # Số 148-150 Cầu Giấy
      [21.035021, 105.794591],  # Ga Chùa Hà
      [21.035899, 105.791805],  # 370 Cầu Giấy
      [21.036538, 105.788421],  # HV Báo chí Tuyên Truyền
      [21.036703, 105.786123],  # Chợ Xanh - Xuân Thủy
      [21.036773, 105.782527],  # Ga ĐHQGHN - Xuân Thủy
      [21.037837, 105.774438],  # Đối diện ĐH Thương Mại
      [21.036283, 105.766393],  # Khoảng Xén Hè Chung Cư A1 - Ngân hàng Vietcombank
      [21.032883, 105.765213],  # Khu đô thị Mỹ Đình II
      [21.029886, 105.762441],  # Nhà C6 KĐT Mỹ Đình I
      [21.031814, 105.756521],  # Qua nhà CT2A, KĐT Xuân Phương 30m
      [21.03703, 105.749095],  # Qua cầu vượt Xuân Phương 100m
      [21.039626, 105.742397],  # Nhà máy Bia Sài Gòn
      [21.042205, 105.737924],  # CN4 Xuân Phương
      [21.047159, 105.736047],  # Đối diện tòa chung cư HaTeCo Group
    ]
  },

  {
    "name": "Bus 55 – TTTM Aeon Mall Long Biên - Cầu Giấy",
    "type": "bus",
    "price": "10.000đ",
    "coords": [
      [21.025573, 105.900174],  # TTTM Aeon Mall Long Biên
      [21.028232, 105.892775],  # Đối diện ngõ 110 Cổ Linh
      [21.029683, 105.884715],  # Đối diện THCS Long Biên
      [21.032953, 105.879889],  # Đối diện công ty Thương mại & Dịch vụ Phương Trâm
      [21.038225, 105.876791],  # Chung cư Golden City
      [21.042350, 105.873779],  # Ngõ 71 Hồng Tiến
      [21.042312, 105.870473],  # Trường Tiểu học Ái Mộ - 135B Nguyễn Văn Cừ
      [21.037730, 105.852988],  # Ô Quan Chưởng
      [21.041380, 105.849584],  # Điểm trung chuyển Long Biên (E1.3)
      [21.044017, 105.847122],  # Dốc Hàng Than
      [21.046368, 105.844185],  # Nhà máy nước Yên Phụ
      [21.050158, 105.840795],  # Đường Yên Phụ - Bãi An Dương
      [21.053903, 105.837543],  # Chợ Yên Phụ
      [21.057112, 105.835697],  # Đền Bảo An, Nghi Tàm
      [21.059869, 105.833887],  # Số 34 Âu Cơ
      [21.063509, 105.831987],  # Số 132 Âu Cơ
      [21.066582, 105.827860],  # Số 236 Âu Cơ - Chợ hoa Quảng An
      [21.073701, 105.824889],  # Số 284 Âu Cơ - Hồ Quảng Bá
      [21.076067, 105.822214],  # Đối diện Đình Nhật Tân
      [21.080536, 105.818647],  # Ngã 3 Lạc Long Quân - Âu Cơ
      [21.076199, 105.814222],  # Đối diện 634-636 Lạc Long Quân
      [21.071529, 105.812111],  # Qua 50m ngõ 677 Lạc Long Quân
      [21.068583, 105.811219],  # Trụ sở Quận uỷ Tây Hồ, Lạc Long Quân
      [21.06602, 105.81032],  # 579 Lạc Long Quân
      [21.063785, 105.809453],  # 545 Lạc Long Quân
      [21.058889, 105.808734],  # Qua ngã 3 Xuân La 70m
      [21.053110, 105.808935],  # Gần ngã 3 Võng Thị
      [21.049057, 105.80656],  # 105 - 111 Lạc Long Quân
      [21.044487, 105.805706],  # Đối diện 528 Đường Bưởi dưới
      [21.039178, 105.806589],  # Đối diện 298 Đường Bưởi dưới
      [21.031306, 105.802546],  # Đối diện Công viên Thủ Lệ - Đường Bưởi dưới
      [21.029334, 105.802879],  # Điểm trung chuyển Cầu Giấy - Nhà ga S8
    ]
  },

  {
    "name": "BRT 01 – Kim Mã – Yên Nghĩa",
    "type": "bus",
    "price": "8.000đ",
    "coords": [
      [20.949605, 105.747615],  # Bến Xe Yên Nghĩa
      [20.956874, 105.757852],  # Nhà chờ Ba La
      [20.960041, 105.76196],  # Nhà chờ Văn La
      [20.96283, 105.764074],  # Nhà chờ Văn Phú
      [20.965408, 105.759546],  # Nhà chờ La Khê
      [20.967681, 105.755459],  # Nhà chờ KĐT Park City
      [20.97026, 105.754685],  # Nhà chờ Cầu La Khê
      [20.973232, 105.757915],  # Nhà chờ An Hưng
      [20.97658, 105.762231],  # Nhà chờ Văn Khê
      [20.979449, 105.765881],  # Nhà chờ Dương Nội
      [20.982277, 105.76979],  # Nhà chờ Vạn Phúc 1
      [20.984819, 105.774834],  # Nhà chờ Vạn Phúc 2
      [20.987907, 105.779352],  # Nhà chờ Mỗ Lao
      [20.990918, 105.783679],  # Nhà chờ Trung Văn
      [20.995336, 105.790943],  # Nhà chờ Lương Thế Vinh
      [20.997771, 105.794523],  # Nhà chờ Khuất Duy Tiến
      [21.002575, 105.800807],  # Nhà chờ Nguyễn Tuân
      [21.00599, 105.805677],  # Nhà chờ Hoàng Đạo Thúy
      [21.013418, 105.812926],  # Nhà chờ Vũ Ngọc Phan
      [21.018132, 105.81599],  # Nhà chờ Thành Công
      [21.031967, 105.829591],  # BRT Giảng Võ
      [21.028844, 105.826306],  # Nhà chờ Núi Trúc
      [21.032089, 105.829172],  # BRT Kim Mã
    ]
  },

  {
    "name": "Metro 2A – Cát Linh - Hà Đông",
    "type": "metro",
    "price": "19.000đ",
    "coords": [
      [21.028355, 105.827262], # Cát Linh
      [21.020154, 105.825349], # La Thành
      [21.014557, 105.819473], # Thái Hà
      [21.006370, 105.816045], # Láng
      [20.997676, 105.812252], # Thượng Đình
      [20.992312, 105.804423], # Vành Đai 3
      [20.984283, 105.793053], # Phùng Khoang
      [20.977714, 105.784800], # Văn Quán
      [20.970218, 105.774964], # Hà Đông
      [20.963843, 105.766796], # La Khê
      [20.955641, 105.756197], # Văn Khê
      [20.949772, 105.748397] # Yên Nghĩa
    ]
  },

  {
      "name": "Metro 3 – Nhổn - Ga Hà Nội",
      "type": "metro",
      "price": "15.000đ",
      "coords": [
      [21.0528834, 105.7348198], # Nhổn
      [21.0480071, 105.7447279], # Minh Khai
      [21.0446728, 105.7532787], # Phú Diễn
      [21.0415186, 105.7618403], # Cầu Diễn
      [21.0382241, 105.7725692], # Lê Đức Thọ
      [21.036692, 105.7824612], # ĐHQG
      [21.0349646, 105.7943165], # Chùa Hà
      [21.0292717, 105.8032107], # Cầu Giấy
      [21.0305635, 105.8163053], # Kim Mã
      [21.0294218, 105.8280265], # Cát Linh
      [21.0279398, 105.8338201], # Văn Miếu
      [21.023954, 105.8415341] # Ga Hà Nội
      ]
  }
]

# FIND MATCHING BUS ROUTES
def find_matching_bus_and_metro_routes(start, end):
    results = []

    # Direct routes
    for r in BUS_AND_METRO_ROUTES:
        if near(start, r["coords"]) and near(end, r["coords"]): # If any station in a bus route is near your starting point and destination
            results.append({
                "type": "direct",
                "routes": [r],
            })

    if results:
        return results

    return results
