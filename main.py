import os
import customtkinter as ctk
from tkintermapview import TkinterMapView
from PIL import ImageTk, Image
from geopy.geocoders import Nominatim
import requests

from bus_routes import find_matching_bus_routes, distance

# APP APPEARANCE
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("theme.json")
BUS_ROUTE_COLORS = ["#1f6aff", "#2ecc71", "#e67e22", "#9b59b6", "#e74c3c"]
WALK_ROUTE_COLORS = ["#0f3c99", "#1f8f4d", "#a3541c", "#6a3b85", "#992d22"]


# GEOCODER (CONVERING TEXT TO LATITUDE AND LONGITUDE)
geolocator = Nominatim(user_agent="vietmove_app", timeout=10)


# VARIABLES
all_bus_routes = []
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
BUS_SPEED  = 20 # km/h

CAR_CO2 = 0.192 # kg CO2/km
BUS_CO2 = 0.082 # kg CO2/km

# LOCATIONS
LOCATIONS = {
    "Hồ Hoàn Kiếm": (21.028866, 105.834708),
    "Nhà hát Lớn": (21.0245, 105.8570),
    "Nhà thờ Lớn": (21.0286457, 105.8488365),
    "Ga Hà Nội": (21.019377, 105.837823),
    "Lăng Bác": (21.0368, 105.8342),
    "Quảng trường Ba Đình": (21.0363, 105.8346),
    "Kim Mã": (21.0336, 105.8142),
    "Giảng Võ": (21.0264, 105.8080),
    "Văn Miếu": (21.0258, 105.8413),
    "Xã Đàn": (21.0161, 105.8281),
    "Láng Hạ": (21.0205, 105.8011),
    "Bách Khoa": (21.004979, 105.841196),
    "Bạch Mai": (21.010567, 105.824891),
    "Đại La": (21.01135, 105.825174),
    "Hồ Tây": (21.0585, 105.8315),
    "Xuân Diệu": (21.0547, 105.8296),
    "Thụy Khuê": (21.0489, 105.8203),
    "Cầu Giấy": (21.0381, 105.7823),
    "Xuân Thủy (ĐHQG)": (21.0381, 105.7823),
    "Khuất Duy Tiến": (21.0124, 105.7905),
    "Ngã Tư Sở": (21.0032, 105.8070),
    "Long Biên": (21.0358, 105.8575),
    "Wellspring Hanoi": (21.039228, 105.873798),
    "Ngọc Thụy": (21.0409, 105.8651),
    "Đức Giang": (21.0423, 105.8691),
    "Bến xe Gia Lâm": (21.0482298, 105.8784425),
    "Gia Lâm": (21.0482, 105.8784),
    "Mai Động": (21.005167, 105.841360),
    "Giáp Bát": (20.9904, 105.8427),
    "Linh Đàm": (20.9718, 105.8397),
    "Hà Đông": (21.0032, 105.7688),
    "Yên Nghĩa": (20.9982, 105.7466),
    "Nam Thăng Long": (21.0602, 105.8128),
    "Nhật Tân": (21.0564, 105.8423),
    "Đông Anh": (21.0912, 105.8065)
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
    Find the nearest bus stop using simple distance
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
    
def estimate_co2(distance, mode):
    if mode == "bus":
        return BUS_CO2 * distance
    elif mode == "car":
        return CAR_CO2 * distance

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
app.title("VietMove")
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

    path_cache.clear()
    all_bus_routes.clear()

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

    matches = find_matching_bus_routes(start, end)

    # Bus routes
    best_bus_co2 = float("inf")
    for i, match in enumerate(matches):
        bus = match["routes"][0]

        color_index = i
        while color_index >= len(BUS_ROUTE_COLORS):
            color_index = color_index - len(BUS_ROUTE_COLORS)

        bus_color = BUS_ROUTE_COLORS[color_index]
        walk_color = WALK_ROUTE_COLORS[color_index]

        start_index = find_closest_stop_index(start, bus["coords"])
        end_index = find_closest_stop_index(end, bus["coords"])

        if start_index == end_index: # If closest start stop is the same as closest end stop, skip this route
            continue

        if start_index > end_index: # Direction check
            start_index, end_index = end_index, start_index
            bus_coords = list(reversed(bus["coords"][start_index:end_index + 1])) # Reverse the bus stops' orders if the passenger travels backwards
        else:
            bus_coords = bus["coords"][start_index:end_index + 1]

        board = bus_coords[0] # The station where you get on the bus
        alight = bus_coords[-1] # The station where you leave the bus

        total_distance = 0
        total_time = 0
        total_co2 = 0
        if total_co2 < best_bus_co2:
            best_bus_co2 = total_co2

        segments = []

        segments.append({ # Path from your starting point to boarding station
            "path": get_cached_path(start, board, "foot"),
            "color": walk_color,
            "width": 3
        })
        total_distance+= distance(start, board)
        total_time+= estimate_time(distance(start, board), "walk")

        for i in range(len(bus_coords) - 1): # For each pair of adjacent bus stops, draw a bus route segment between them.
            a = bus_coords[i]
            b = bus_coords[i + 1]
            total_distance+= distance(a, b)
            total_time+= estimate_time(distance(a, b), "bus")
            total_co2+= estimate_co2(distance(a, b), "bus")

            segments.append({
                "path": get_cached_path(a, b, "driving"),
                "color": bus_color,
                "width": 5
            })

        segments.append({ # Path from leaving station to your destination
            "path": get_cached_path(alight, end, "foot"),
            "color": walk_color,
            "width": 3
        })
        total_distance+= distance(alight, end)
        total_time+= estimate_time(distance(alight, end), "walk")

        all_bus_routes.append({ # Connect all the paths' segments together
            "segments": segments,
            "board": board,
            "alight": alight
        })

        route_index = len(all_bus_routes) - 1

        ctk.CTkButton(
            routes_panel,
            text=f"🚍 {bus['name']}\n⏱️ {round(total_time, 1)} phút   💰 {bus['price']}   ↔️ {round(total_distance, 1)} km   🏭 {round(total_co2, 2)} kg CO2",
            command=lambda id=route_index: show_bus_route(id),
            anchor="w",
            height=54
        ).pack(fill="x", pady=6)
    
    # Driving
    total_distance = 0
    total_time = 0
    total_co2 = 0
    car_path = get_cached_path(start, end, "driving")

    car_route = {
        "segments": [{
            "path": car_path,
            "color": "#f1c40f",
            "width": 5
        }]
    }
    total_distance+= distance(start, end)
    total_time+= estimate_time(distance(start, end), "car")
    total_co2+= estimate_co2(distance(start, end), "car")

    if best_bus_co2 < float("inf"):
        update_eco_message(best_bus_co2, total_co2)
    else:
        eco_label.configure(
            text="🌍 Xe buýt giúp giảm ùn tắc và phát thải.\nHãy chọn giao thông công cộng khi có thể."
        )

    ctk.CTkButton(
        routes_panel,
        text=f"🚗 Ôtô\n⏱️ {round(total_time, 1)} phút   ↔️ {round(total_distance, 1)} km   🏭 {round(total_co2, 2)} kg CO2",
        command=lambda: show_car_route(),
        anchor="w"
    ).pack(fill="x", pady=6)


# DISPLAY ROUTE ON MAP
def show_bus_route(index):
    """
    Draw selected route on map
    """
    global board_marker, alight_marker

    map_widget.delete_all_path()

    if board_marker:
        board_marker.delete()
    if alight_marker:
        alight_marker.delete()

    route = all_bus_routes[index]

    # Draw walking paths first
    for segment in route["segments"]:
        if segment["width"] == 3:
            map_widget.set_path(
                segment["path"],
                width=segment["width"],
                color=segment["color"]
            )

    # Draw bus paths second
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
