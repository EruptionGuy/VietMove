import os
import customtkinter as ctk
from tkintermapview import TkinterMapView
from PIL import ImageTk, Image
from geopy.geocoders import Nominatim
import requests

from bus_routes import find_matching_bus_and_metro_routes, distance

# APP APPEARANCE
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("theme.json")
BUS_AND_METRO_ROUTE_COLORS = ["#1f6aff", "#2ecc71", "#e67e22", "#9b59b6", "#e74c3c"]
WALK_ROUTE_COLORS = ["#0f3c99", "#1f8f4d", "#a3541c", "#6a3b85", "#992d22"]


# GEOCODER (CONVERING TEXT TO LATITUDE AND LONGITUDE)
geolocator = Nominatim(user_agent="vietmove_app", timeout=10)


# VARIABLES
all_bus_and_metro_routes = []
car_route = None

start_position = None
end_position = None

start_marker = None
end_marker = None
board_marker = None
alight_marker = None

path_cache = {}

WALK_SPEED = 5 # km/h
CAR_SPEED = 25 # km/h
BUS_SPEED  = 25 # km/h
METRO_SPEED = 35 # km/h

CAR_CO2 = 0.192 # kg CO2/km
BUS_CO2 = 0.082 # kg CO2/km
METRO_CO2 = 0.035 # kg CO2/km

# LOCATIONS
LOCATIONS = {
    # Central / Old Quarter
    "Hồ Hoàn Kiếm": (21.031869, 105.851646),
    "Đền Ngọc Sơn": (21.030758, 105.852547),
    "Nhà hát Lớn Hà Nội": (21.024324, 105.857616),
    "Nhà thờ Lớn Hà Nội": (21.028786, 105.848834),
    "Phố Tràng Tiền": (21.024800, 105.855568),

    # Stations & Interchanges
    "Ga Hà Nội": (21.023954, 105.841534),
    "Ga Cát Linh (Metro 2A)": (21.028355, 105.827262),
    "Ga Kim Mã (Metro 3)": (21.030564, 105.816305),
    "Ga Cầu Giấy (Metro 3)": (21.029272, 105.803211),
    "Ga Văn Miếu (Metro 3)": (21.027940, 105.833820),

    # Ba Đình
    "Lăng Chủ tịch Hồ Chí Minh": (21.036856, 105.834690),
    "Quảng trường Ba Đình": (21.037245, 105.836317),
    "Phủ Chủ tịch": (21.039394, 105.835059),
    "Công viên Lênin": (21.031265, 105.839447),

    # Parks & Green Spaces
    "Công viên Thống Nhất": (21.016960, 105.844346),
    "Vườn Bách Thảo": (21.041221, 105.830287),
    "Công viên Cầu Giấy": (21.028326, 105.790851),
    "Công viên Nghĩa Đô": (21.040581, 105.796479),
    "Vườn hoa Hoàng Cầu": (21.016792, 105.821007),
    "Vườn hoa Lý Thái Tổ": (21.027523, 105.854235),
    "Công viên Long Biên": (21.060986, 105.904675),

    # West / Inner West
    "Phố Kim Mã": (21.030703, 105.817295),
    "Phố Giảng Võ": (21.028056, 105.825308),
    "Phố Láng Hạ": (21.017048, 105.815421),
    "Ngã Tư Sở": (21.003133, 105.820775),

    # Education – Universities
    "ĐH Bách Khoa Hà Nội": (21.005092, 105.841546),
    "ĐH Kinh tế Quốc dân": (21.000055, 105.842498),
    "ĐH Xây dựng Hà Nội": (21.003314, 105.843477),
    "ĐH Ngoại thương": (21.023039, 105.805449),
    "ĐH Giao thông Vận tải": (21.028155, 105.803404),
    "ĐHQG Hà Nội (Xuân Thủy)": (21.036692, 105.782461),

    # Education – Schools
    "THPT Chu Văn An": (21.043133, 105.832555),
    "THPT Việt Đức": (21.023516, 105.849321),
    "THPT Kim Liên": (21.010933, 105.831671),
    "Wellspring Hanoi": (21.039228, 105.873798),
    "Hanoi International School": (21.033734, 105.813524),
    "UNIS Hanoi": (21.074986, 105.809079),
    "Vietnam-Australia School": (21.032664, 105.763099),

    # South
    "Phố Xã Đàn": (21.012908, 105.835491),
    "Phố Đại La": (20.996640, 105.846256),
    "Phố Bạch Mai": (21.002220, 105.850828),
    "Phố Mai Động": (20.989237, 105.861325),
    "Phố Giáp Bát": (20.985253, 105.843581),
    "Phố Linh Đàm": (20.964956, 105.824845),
    "Times City": (20.997991, 105.867556),

    # Hà Đông / Southwest
    "Ga Hà Đông": (20.970218, 105.774964),
    "Ga Văn Quán": (20.977714, 105.784800),
    "Ga Phùng Khoang": (20.984283, 105.793053),
    "Ga Yên Nghĩa": (20.998200, 105.746600),

    # West Lake / North
    "Sheraton Hanoi Hotel": (21.060230, 105.830855),
    "Đường Xuân Diệu": (21.064393, 105.828152),
    "Đường Thụy Khuê": (21.043413, 105.821139),
    "Lotte Mall Tây Hồ": (21.076277, 105.811735),

    # Long Biên / East
    "Bến xe Long Biên": (21.041237, 105.849587),
    "Aeon Mall Long Biên": (21.027474, 105.898980),
    "Đường Long Biên": (21.040900, 105.865100),
    "Đường Ngô Gia Tự": (21.065769, 105.898262),
    "Đường Nguyễn Văn Cừ": (21.046488, 105.877367),
    "Bến xe Gia Lâm": (21.048230, 105.878443),
}


# HELPER FUNCTIONS
def fetch_path(start, end, mode):
    """
    Get a path from OpenStreetMap routing (OSRM)
    """
    url = f"https://router.project-osrm.org/route/v1/{mode}/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full&geometries=geojson"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    coordinates = response.json()["routes"][0]["geometry"]["coordinates"]

    # Convert (lon, lat) into (lat, lon)
    converted_path = []

    for lon, lat in coordinates:
        converted_path.append((lat, lon))

    return converted_path


def get_cached_path(start, end, mode):
    """
    Save paths so we don’t request the same route twice
    """
    key = (tuple(start), tuple(end), mode)

    if key not in path_cache:
        path_cache[key] = fetch_path(start, end, mode)

    return path_cache[key]


def find_closest_stop_index(point, stops):
    """
    Find the nearest stop using simple distance
    """
    closest_index = 0
    smallest_distance = float("inf") # Sets initial value to infinity to guarantee that the first real distance will be smaller

    for i, stop in enumerate(stops):
        dx = point[0] - stop[0]
        dy = point[1] - stop[1]
        distance = dx * dx + dy * dy # Applying distance formula

        if distance < smallest_distance:
            smallest_distance = distance
            closest_index = i

    return closest_index

def estimate_time(distance, mode):
    if mode == "walk":
        return distance / WALK_SPEED * 60
    elif mode == "bus":
        return distance / BUS_SPEED * 60
    elif mode == "car":
        return distance / CAR_SPEED * 60
    elif mode == "metro":
        return distance / METRO_SPEED * 60
    
def estimate_co2(distance, mode):
    if mode == "bus":
        return BUS_CO2 * distance
    elif mode == "car":
        return CAR_CO2 * distance
    elif mode == "metro":
        return METRO_CO2 * distance

def update_eco_message(bus_co2, car_co2):
    saved = max(car_co2 - bus_co2, 0)

    eco_label.configure(
        text=(
            f"🌱 Nếu bạn đi xe buýt, bạn đã giảm khoảng {round(saved, 2)} kg CO₂ so với ô tô.\n"
            f"Môi trường cần bạn — và Việt Nam cũng vậy 🇻🇳"
        )
    )

# USER INTERFACE
app = ctk.CTk()
app.title("VietMove – Smart Transit Planner")
app.geometry("1200x720")
app.iconphoto(False, ImageTk.PhotoImage(file=os.path.join("app-icon.png")))

app.grid_columnconfigure(0, weight=0)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# Sidebar
sidebar = ctk.CTkFrame(app, width=400, corner_radius=0)
sidebar.grid(row=0, column=0, sticky="ns")
sidebar.grid_propagate(False)
sidebar.pack_propagate(False)

ctk.CTkLabel(
    sidebar,
    text="VietMove",
    font=ctk.CTkFont(size=28, weight="bold")
).pack(pady=(25, 15))

input_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
input_frame.pack(fill="x", padx=20)

start_dropdown = ctk.CTkOptionMenu(
    input_frame,
    values=list(LOCATIONS.keys())
)
start_dropdown.pack(fill="x", pady=(0, 10))

end_dropdown = ctk.CTkOptionMenu(
    input_frame,
    values=list(LOCATIONS.keys())
)
end_dropdown.pack(fill="x")

loading_label = ctk.CTkLabel(
    sidebar,
    text="",
    text_color="#bbbbbb",
    wraplength=400 - 40
)
loading_label.pack(pady=(0, 10))

routes_panel = ctk.CTkScrollableFrame(
    sidebar,
    fg_color="transparent",
    scrollbar_button_color="#9e3232",
    scrollbar_button_hover_color="#b63a3a"
)
routes_panel.pack(fill="both", expand=True, padx=15, pady=(0, 15))

eco_label = ctk.CTkLabel(
    sidebar,
    text="🌱 Chọn xe buýt để giảm phát thải CO₂.\nMỗi chuyến đi bền vững là một bước cho Việt Nam xanh hơn.",
    text_color="#8dd98d",
    font=ctk.CTkFont(size=12),
    wraplength=360,
    justify="center"
)
eco_label.pack(side="bottom", pady=12)

# Map
map_widget = TkinterMapView(app, corner_radius=0)
map_widget.grid(row=0, column=1, sticky="nsew")
map_widget.set_position(21.0285, 105.8542)
map_widget.set_zoom(12)

# Buttons
def on_search_clicked():
    """
    User presses 'Tìm lộ trình'
    """
    loading_label.configure(text="⏳ Đang tải lộ trình...")
    app.after(100, search_routes)


def search_routes():
    """
    Convert text → coordinates (Hanoi only)
    """
    start_name = start_dropdown.get()
    end_name = end_dropdown.get()

    if start_name == end_name:
        loading_label.configure(text="❌ Điểm đi và điểm đến trùng nhau")
        return

    start_coords = LOCATIONS[start_name]
    end_coords = LOCATIONS[end_name]

    prepare_routes(start_coords, end_coords)
    loading_label.configure(text="🚍 Bấm vào các lộ trình để xem đường đi")

ctk.CTkButton(
    sidebar,
    text="Tìm lộ trình",
    height=42,
    command=on_search_clicked
).pack(padx=20, pady=16, fill="x")


# ROUTE BUILDING
def prepare_routes(start, end):
    """
    Build all possible routes
    """
    global start_position, end_position, start_marker, end_marker, car_route

    # path_cache.clear()
    all_bus_and_metro_routes.clear()

    start_position = start
    end_position = end

    map_widget.delete_all_path()

    for widget in routes_panel.winfo_children():
        widget.destroy()

    if start_marker:
        start_marker.delete()
    if end_marker:
        end_marker.delete()

    start_marker = map_widget.set_marker(*start, text="📍 Start")
    end_marker = map_widget.set_marker(*end, text="🏁 Destination")

    matches = find_matching_bus_and_metro_routes(start, end)

    # Bus and metro routes
    best_co2 = float("inf")

    for i, match in enumerate(matches):
        bus_and_metro = match["routes"][0]

        color_index = i
        while color_index >= len(BUS_AND_METRO_ROUTE_COLORS):
            color_index = color_index - len(BUS_AND_METRO_ROUTE_COLORS)

        bus_and_metro_color = BUS_AND_METRO_ROUTE_COLORS[color_index]
        walk_color = WALK_ROUTE_COLORS[color_index]

        start_index = find_closest_stop_index(start, bus_and_metro["coords"])
        end_index = find_closest_stop_index(end, bus_and_metro["coords"])

        if start_index == end_index:  # If closest start stop is the same as closest end stop, skip this route
            continue

        if start_index > end_index:  # Direction check
            start_index, end_index = end_index, start_index
            bus_and_metro_coords = list(
                reversed(bus_and_metro["coords"][start_index:end_index + 1])
            )  # Reverse the stops' orders if the passenger travels backwards
        else:
            bus_and_metro_coords = bus_and_metro["coords"][start_index:end_index + 1]

        board = bus_and_metro_coords[0]   # The station where you get on the bus/metro
        alight = bus_and_metro_coords[-1] # The station where you leave the bus/metro

        total_distance = 0
        total_time = 0
        total_co2 = 0

        segments = []

        segments.append({  # Path from your starting point to boarding station
            "path": get_cached_path(start, board, "foot"),
            "color": walk_color,
            "width": 3
        })
        total_distance += distance(start, board)
        total_time += estimate_time(distance(start, board), "walk")

        for i in range(len(bus_and_metro_coords) - 1):  # For each pair of adjacent bus/metro stops
            a = bus_and_metro_coords[i]
            b = bus_and_metro_coords[i + 1]

            d = distance(a, b)
            total_distance += d
            total_time += estimate_time(d, bus_and_metro["type"])
            total_co2 += estimate_co2(d, bus_and_metro["type"])

            if bus_and_metro["type"] == "bus":
                segments.append({
                    "path": get_cached_path(a, b, "driving"),
                    "color": bus_and_metro_color,
                    "width": 5
                })
            elif bus_and_metro["type"] == "metro":
                segments.append({
                    "path": [a, b],  # Draw straight paths between metro stations since OSRM does not support 'metro' mode
                    "color": bus_and_metro_color,
                    "width": 5
                })

        segments.append({  # Path from leaving station to your destination
            "path": get_cached_path(alight, end, "foot"),
            "color": walk_color,
            "width": 3
        })
        total_distance += distance(alight, end)
        total_time += estimate_time(distance(alight, end), "walk")

        # Update best CO2
        best_co2 = min(best_co2, total_co2)

        all_bus_and_metro_routes.append({  # Connect all the paths' segments together
            "segments": segments,
            "board": board,
            "alight": alight
        })

        route_index = len(all_bus_and_metro_routes) - 1

        emoji = "🚍" if bus_and_metro["type"] == "bus" else "🚇"
        ctk.CTkButton(
            routes_panel,
            text=f"{emoji} {bus_and_metro['name']}\n"
                f"⏱️ {round(total_time, 1)} phút   "
                f"💰 {bus_and_metro['price']}   "
                f"↔️ {round(total_distance, 1)} km   "
                f"🏭 {round(total_co2, 2)} kg CO2",
            command=lambda id=route_index: show_bus_and_metro_route(id),
            anchor="w",
            height=54
        ).pack(fill="x", pady=6)

    # Driving or walking (if start and destination are close together)
    car_distance = distance(start, end)
    car_co2 = estimate_co2(car_distance, "car")

    if car_distance < 3:
        car_time = estimate_time(car_distance, "walk")

        car_route = {
            "segments": [{
                "path": get_cached_path(start, end, "foot"),
                "color": "#069494",
                "width": 5
            }]
        }

        ctk.CTkButton(
            routes_panel,
            text=f"🚶‍♂️ Đi bộ\n⏱️ {round(car_time, 1)} phút   ↔️ {round(car_distance, 1)} km",
            command=show_car_route,
            anchor="w"
        ).pack(fill="x", pady=6)
    else:
        car_time = estimate_time(car_distance, "car")

        car_route = {
            "segments": [{
                "path": get_cached_path(start, end, "driving"),
                "color": "#f1c40f",
                "width": 5
            }]
        }

        ctk.CTkButton(
            routes_panel,
            text=f"🚗 Ôtô\n⏱️ {round(car_time, 1)} phút   ↔️ {round(car_distance, 1)} km   "
                f"🏭 {round(car_co2, 2)} kg CO2",
            command=show_car_route,
            anchor="w"
        ).pack(fill="x", pady=6)

    # Environmental message
    if best_co2 < float("inf"):
        update_eco_message(best_co2, car_co2)
    else:
        eco_label.configure(
            text="🌍 Xe buýt giúp giảm ùn tắc và phát thải.\nHãy chọn giao thông công cộng khi có thể."
        )

    # Fit bounding box
    map_widget.set_position(start[0], start[1])
    map_widget.set_zoom(15)



# DISPLAY ROUTE ON MAP
def show_bus_and_metro_route(index):
    """
    Draw selected route on map
    """
    global board_marker, alight_marker

    map_widget.delete_all_path()

    if board_marker:
        board_marker.delete()
    if alight_marker:
        alight_marker.delete()

    route = all_bus_and_metro_routes[index]

    # Draw walking paths first
    for segment in route["segments"]:
        if segment["width"] == 3:
            map_widget.set_path(
                segment["path"],
                width=segment["width"],
                color=segment["color"]
            )

    # Draw bus/metro paths second
    for segment in route["segments"]:
        if segment["width"] == 5:
            map_widget.set_path(
                segment["path"],
                width=segment["width"],
                color=segment["color"]
            )

    if "board" in route:
        board_marker = map_widget.set_marker(*route["board"], text="🟢 Lên xe")
        alight_marker = map_widget.set_marker(*route["alight"], text="🔴 Xuống xe")

def show_car_route():
    """
    Draw selected car route on map
    """
    global board_marker, alight_marker

    map_widget.delete_all_path()

    if board_marker:
        board_marker.delete()
    if alight_marker:
        alight_marker.delete()

    for segment in car_route["segments"]:
        if segment["width"] == 5:
            map_widget.set_path(
                segment["path"],
                width=segment["width"],
                color=segment["color"]
            )

# START APP
app.mainloop()
