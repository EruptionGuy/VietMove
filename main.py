import os
import json
import random
import customtkinter as ctk
from tkintermapview import TkinterMapView
from PIL import ImageTk, Image
from geopy.geocoders import Nominatim
import requests

from bus_routes import find_matching_bus_and_metro_routes, distance, BUS_AND_METRO_ROUTES

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
transfer_marker = None

path_cache = {}

try:
    with open("precomputed_routes.json", "r") as f:
        PRECOMPUTED = json.load(f)
except:
    PRECOMPUTED = {}

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
def format_coord(coord):
    return f"{coord[0]:.6f},{coord[1]:.6f}"

def fetch_path(start, end, mode):
    """
    Get a path from OpenStreetMap routing (OSRM)
    """
    url = f"http://router.project-osrm.org/route/v1/{mode}/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full&geometries=geojson"

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

    if key in path_cache:
        return path_cache[key]

    # Use precomputed routes to reduce API requests
    if mode == "driving":
        key_str = f"{format_coord(start)}-{format_coord(end)}"
        reverse_key_str = f"{format_coord(end)}-{format_coord(start)}"

        if key_str in PRECOMPUTED:
            path_cache[key] = PRECOMPUTED[key_str]
            print("✅ Found precomputed route")
            return path_cache[key]

        elif reverse_key_str in PRECOMPUTED:
            path_cache[key] = list(reversed(PRECOMPUTED[reverse_key_str]))
            print("✅ Found precomputed route (reversed)")
            return path_cache[key]

        print("❌ Couldn't find precomputed route")

    # fallback to OSRM
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

def find_transfer(route1, route2, max_dist=0.3):
    """
    Find a transfer point between two routes (shared or nearby stops)
    """
    for i, a in enumerate(route1["coords"]):
        for j, b in enumerate(route2["coords"]):
            if distance(a, b) < max_dist:
                return i, j  # indices in both routes

    return None

def find_routes_with_transfer(start, end):
    results = []

    for route1 in BUS_AND_METRO_ROUTES:
        for route2 in BUS_AND_METRO_ROUTES:

            # Skip same route
            if route1 == route2:
                continue

            transfer = find_transfer(route1, route2)
            if not transfer:
                continue

            i1, i2 = transfer

            # Find closest stops
            start_idx = find_closest_stop_index(start, route1["coords"])
            end_idx = find_closest_stop_index(end, route2["coords"])

            # Ensure valid direction
            # Must move forward on both routes
            if start_idx >= i1 or i2 >= end_idx:
                continue

            # Limit how far along the route we go before transfer
            if (i1 - start_idx) > 15:
                continue

            # Limit how far after transfer to destination
            if (end_idx - i2) > 15:
                continue

            results.append({
                "route1": route1,
                "route2": route2,
                "start_idx": start_idx,
                "transfer_idx1": i1,
                "transfer_idx2": i2,
                "end_idx": end_idx
            })

    return results

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
    loading_label.configure(text="Bấm vào các lộ trình để xem đường đi")

ctk.CTkButton(
    sidebar,
    text="Tìm lộ trình",
    height=42,
    command=on_search_clicked
).pack(padx=20, pady=16, fill="x")


def build_direct_route(start, end, bus_and_metro):
    """
    Build ONE direct route (simplified)
    """
    coords = bus_and_metro["coords"]

    start_index = find_closest_stop_index(start, coords)
    end_index = find_closest_stop_index(end, coords)

    # Skip useless route
    if start_index == end_index:
        return None

    # Ensure correct direction
    if start_index > end_index:
        coords = list(reversed(coords[end_index:start_index + 1]))
    else:
        coords = coords[start_index:end_index + 1]

    board = coords[0]
    alight = coords[-1]

    segments = []
    total_distance = 0
    total_time = 0
    total_co2 = 0

    if distance(start, board) > 0.8:  # 800m max
        return None

    # Walk to bus stop
    segments.append({
        "path": get_cached_path(start, board, "foot"),
        "color": "#888",
        "width": 3
    })
    total_distance += distance(start, board)
    total_time += estimate_time(distance(start, board), "walk")

    # Bus/metro segment
    route_color = BUS_AND_METRO_ROUTE_COLORS[random.randint(0, len(BUS_AND_METRO_ROUTE_COLORS)-1)]
    for i in range(len(coords) - 1):
        a = coords[i]
        b = coords[i + 1]

        d = distance(a, b)
        total_distance += d
        total_time += estimate_time(d, bus_and_metro["type"])
        total_co2 += estimate_co2(d, bus_and_metro["type"])

        segments.append({
            "path": get_cached_path(a, b, "driving"),
            "color": route_color,
            "width": 5
        })

    # Reject if walking too far after getting off
    if distance(alight, end) > 0.8:
        return None

    # Walk to destination
    segments.append({
        "path": get_cached_path(alight, end, "foot"),
        "color": "#888",
        "width": 3
    })
    total_distance += distance(alight, end)
    total_time += estimate_time(distance(alight, end), "walk")

    return {
        "segments": segments,
        "board": board,
        "alight": alight,
        "distance": total_distance,
        "time": total_time,
        "co2": total_co2,
        "name": bus_and_metro["name"],
        "type": bus_and_metro["type"],
        "price": int(bus_and_metro["price"])
    }

# ROUTE BUILDING
def prepare_routes(start, end):
    """
    Build all possible routes (simplified)
    """
    global start_marker, end_marker, car_route

    path_cache.clear()
    all_bus_and_metro_routes.clear()

    map_widget.delete_all_path()

    for widget in routes_panel.winfo_children():
        widget.destroy()

    # Markers
    if start_marker:
        start_marker.delete()
    if end_marker:
        end_marker.delete()

    start_marker = map_widget.set_marker(*start, text="📍 Điểm đi")
    end_marker = map_widget.set_marker(*end, text="🏁 Điểm đến")

    matches = find_matching_bus_and_metro_routes(start, end)

    best_co2 = float("inf")

    # 🚍 DIRECT ROUTES
    for match in matches:
        route = build_direct_route(start, end, match["routes"][0])

        if not route:
            continue

        best_co2 = min(best_co2, route["co2"])

        all_bus_and_metro_routes.append(route)
        route_index = len(all_bus_and_metro_routes) - 1

        emoji = "🚍" if route["type"] == "bus" else "🚇"

        ctk.CTkButton(
            routes_panel,
            text=f"{emoji} {route['name']}\n"
                 f"⏱️ {round(route['time'],1)} phút   "
                 f"💰 {route['price']} VND\n"
                 f"↔️ {round(route['distance'],1)} km   "
                 f"🏭 {round(route['co2'],2)} kg CO2",
            command=lambda id=route_index: show_bus_and_metro_route(id),
            anchor="center"
        ).pack(fill="x", pady=6)

    # 🔁 TRANSFER ROUTES
    transfer_matches = find_routes_with_transfer(start, end)

    for match in transfer_matches[:3]:
        total_distance = 0
        total_time = 0
        total_co2 = 0
        total_price = 0

        route1 = match["route1"]
        route2 = match["route2"]

        coords1 = route1["coords"]
        coords2 = route2["coords"]

        part1 = coords1[match["start_idx"]:match["transfer_idx1"] + 1]
        part2 = coords2[match["transfer_idx2"]:match["end_idx"] + 1]

        transfer_point = part1[-1]

        walk_start = distance(start, part1[0])
        walk_transfer = distance(part1[-1], part2[0])
        walk_end = distance(part2[-1], end)

        if walk_start > 0.8:
            continue

        if walk_transfer > 0.8:
            continue

        if walk_end > 0.8:
            continue

        segments = []

        # Walk to first route
        segments.append({
            "path": get_cached_path(start, part1[0], "foot"),
            "color": "#888",
            "width": 3
        })

        total_distance += walk_start
        total_time += estimate_time(walk_start, "walk")

        # First route
        for i in range(len(part1) - 1):
            a = part1[i]
            b = part1[i + 1]

            d = distance(a, b)
            total_distance += d
            total_time += estimate_time(d, route1["type"])
            total_co2 += estimate_co2(d, route1["type"])

            segments.append({
                "path": get_cached_path(a, b, "driving"),
                "color": "#3498db",
                "width": 5
            })

        total_price += route1["price"]

        # Transfer walk
        segments.append({
            "path": get_cached_path(part1[-1], part2[0], "foot"),
            "color": "#aaaaaa",
            "width": 3
        })

        total_distance += walk_transfer
        total_time += estimate_time(walk_transfer, "walk")

        # Second route
        for i in range(len(part2) - 1):
            a = part2[i]
            b = part2[i + 1]

            d = distance(a, b)
            total_distance += d
            total_time += estimate_time(d, route2["type"])
            total_co2 += estimate_co2(d, route2["type"])

            segments.append({
                "path": get_cached_path(a, b, "driving"),
                "color": "#e67e22",
                "width": 5
            })

        total_price += route2["price"]

        # Walk to destination
        segments.append({
            "path": get_cached_path(part2[-1], end, "foot"),
            "color": "#888",
            "width": 3
        })

        total_distance += walk_end
        total_time += estimate_time(walk_end, "walk")

        all_bus_and_metro_routes.append({
            "segments": segments,
            "board": part1[0],
            "transfer": transfer_point,
            "alight": part2[-1],
            "distance": total_distance,
            "time": total_time,
            "co2": total_co2,
            "price": total_price
        })

        route_index = len(all_bus_and_metro_routes) - 1

        ctk.CTkButton(
            routes_panel,
            text=f"🔁 {route1['name']}\n→ {route2['name']}\n"
                f"⏱️ {round(total_time,1)} phút   "
                f"💰 {total_price} VND \n"
                f"↔️ {round(total_distance,1)} km   "
                f"🏭 {round(total_co2,2)} kg CO2",
            command=lambda id=route_index: show_bus_and_metro_route(id),
            anchor="center"
        ).pack(fill="x", pady=6)
   
    car_distance = distance(start, end)
    car_co2 = estimate_co2(car_distance, "car")

    if car_distance < 2:
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
            anchor="center"
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
            text=f"🚗 Ô tô\n"
                f"⏱️ {round(car_time,1)} phút   "
                f"↔️ {round(car_distance,1)} km   "
                f"🏭 {round(car_co2,2)} kg CO2",
            command=show_car_route,
            anchor="center"
        ).pack(fill="x", pady=6)

    if best_co2 < float("inf"):
        update_eco_message(best_co2, car_co2)

    # map view
    map_widget.set_position(start[0], start[1])
    map_widget.set_zoom(15)

# DISPLAY ROUTE ON MAP
def show_bus_and_metro_route(index):
    global board_marker, alight_marker, transfer_marker

    map_widget.delete_all_path()

    if board_marker:
        board_marker.delete()
    if alight_marker:
        alight_marker.delete()
    if transfer_marker:
        transfer_marker.delete()

    route = all_bus_and_metro_routes[index]

    # Draw walking paths first
    for segment in route["segments"]:
        if segment["width"] == 3:
            map_widget.set_path(
                segment["path"],
                width=segment["width"],
                color=segment["color"]
            )

    # Draw bus/metro paths
    for segment in route["segments"]:
        if segment["width"] == 5:
            map_widget.set_path(
                segment["path"],
                width=segment["width"],
                color=segment["color"]
            )

    # Markers
    if "board" in route:
        board_marker = map_widget.set_marker(*route["board"], text="🟢 Lên xe")
        alight_marker = map_widget.set_marker(*route["alight"], text="🔴 Xuống xe")

    # ✅ Transfer marker
    if "transfer" in route:
        transfer_marker = map_widget.set_marker(
            *route["transfer"],
            text="🔄 Chuyển tuyến"
        )

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
