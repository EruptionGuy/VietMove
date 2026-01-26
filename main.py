import customtkinter as ctk
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim
import requests

from bus_routes import find_matching_bus_routes

# APP APPEARANCE
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
BUS_ROUTE_COLORS = ["#1f6aff", "#2ecc71", "#e67e22", "#9b59b6", "#e74c3c"]
WALK_ROUTE_COLORS = ["#0f3c99", "#1f8f4d", "#a3541c", "#6a3b85", "#992d22"]


# GEOCODER (CONVERING TEXT TO LATITUDE AND LONGITUDE)
geolocator = Nominatim(user_agent="vietmove_app", timeout=10)


# VARIABLES
all_routes = []

start_position = None
end_position = None

start_marker = None
end_marker = None
board_marker = None
alight_marker = None

path_cache = {}


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


# USER INTERFACE
app = ctk.CTk()
app.title("VietMove")
app.geometry("1200x720")

app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# Sidebar
sidebar = ctk.CTkFrame(app, width=320, corner_radius=0)
sidebar.grid(row=0, column=0, sticky="ns")

ctk.CTkLabel(
    sidebar,
    text="VietMove",
    font=ctk.CTkFont(size=28, weight="bold")
).pack(pady=(25, 15))

start_entry = ctk.CTkEntry(sidebar, placeholder_text="Bạn đang ở đâu?")
start_entry.pack(padx=20, pady=8)

end_entry = ctk.CTkEntry(sidebar, placeholder_text="Bạn muốn đi đâu?")
end_entry.pack(padx=20, pady=8)

loading_label = ctk.CTkLabel(sidebar, text="")
loading_label.pack(pady=5)

routes_panel = ctk.CTkFrame(sidebar, fg_color="transparent")
routes_panel.pack(fill="both", expand=True, padx=15)

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
    start_text = start_entry.get().strip() + ", Hà Nội, 11120, Vietnam"
    end_text = end_entry.get().strip() + ", Hà Nội, 11120, Vietnam"

    start_location = geolocator.geocode(start_text)
    end_location = geolocator.geocode(end_text)

    if not start_location or not end_location:
        loading_label.configure(text="❌ Không tìm thấy địa điểm")
        return

    start_coords = (start_location.latitude, start_location.longitude)
    end_coords = (end_location.latitude, end_location.longitude)

    prepare_routes(start_coords, end_coords)
    loading_label.configure(text="")

ctk.CTkButton(
    sidebar,
    text="Tìm lộ trình",
    height=42,
    command=on_search_clicked
).pack(padx=20, pady=16, fill="x")


# ROUTE BUILDING
def prepare_routes(start_coords, end_coords):
    """
    Build all possible routes (direct bus OR transfer bus routes)
    and create buttons for the user to select them.
    """

    # We modify global variables, so we must declare them
    global start_position, end_position
    global start_marker, end_marker
    global all_routes

    # --------------------------------
    # 1️⃣ Reset old data
    # --------------------------------

    path_cache.clear()        # Clear saved paths
    all_routes.clear()        # Remove old routes

    start_position = start_coords
    end_position = end_coords

    # Clear everything drawn on the map
    map_widget.delete_all_path()

    # Remove old route buttons
    for widget in routes_panel.winfo_children():
        widget.destroy()

    # Remove old markers (if they exist)
    if start_marker:
        start_marker.delete()
    if end_marker:
        end_marker.delete()

    # Add start & destination markers
    start_marker = map_widget.set_marker(*start_coords, text="📍 Start")
    end_marker = map_widget.set_marker(*end_coords, text="🏁 Destination")

    # --------------------------------
    # 2️⃣ Find matching bus routes
    # --------------------------------

    matches = find_matching_bus_routes(start_coords, end_coords)

    # --------------------------------
    # 3️⃣ If NO bus routes → drive only
    # --------------------------------

    if not matches:
        car_path = get_cached_path(start_coords, end_coords, "driving")

        all_routes.append({
            "segments": [{
                "path": car_path,
                "color": "#f1c40f",
                "width": 5
            }]
        })

        ctk.CTkButton(
            routes_panel,
            text="🚗 Đi thẳng bằng ô tô",
            command=lambda: show_route(0),
            anchor="w"
        ).pack(fill="x", pady=6)

        show_route(0)
        return

    # --------------------------------
    # 4️⃣ Handle BUS routes (direct OR transfer)
    # --------------------------------

    for route_index, match in enumerate(matches):

        buses = match["routes"]     # 1 bus (direct) or 2 buses (transfer)
        transfer_point = match["transfer"]

        bus_color = BUS_ROUTE_COLORS[route_index % len(BUS_ROUTE_COLORS)]
        walk_color = WALK_ROUTE_COLORS[route_index % len(WALK_ROUTE_COLORS)]

        segments = []               # All drawing pieces for this route
        current_position = start_coords  # Where the user currently is

        # --------------------------------
        # 5️⃣ Loop through each bus
        # --------------------------------

        for bus_number, bus in enumerate(buses):

            # Find closest stop to where we are now
            start_stop_index = find_closest_stop_index(
                current_position, bus["coords"]
            )

            # Decide where to get off
            if bus_number == len(buses) - 1:
                # Last bus → get off near destination
                end_stop_index = find_closest_stop_index(
                    end_coords, bus["coords"]
                )
            else:
                # Transfer bus → get off near transfer point
                end_stop_index = find_closest_stop_index(
                    transfer_point, bus["coords"]
                )

            # Ignore broken routes
            if start_stop_index == end_stop_index:
                continue

            # Make sure stops are in correct order
            if start_stop_index > end_stop_index:
                bus_stops = list(
                    reversed(bus["coords"][end_stop_index:start_stop_index + 1])
                )
            else:
                bus_stops = bus["coords"][start_stop_index:end_stop_index + 1]

            board_stop = bus_stops[0]
            alight_stop = bus_stops[-1]

            # --------------------------------
            # 6️⃣ Walk to the bus stop
            # --------------------------------

            segments.append({
                "path": get_cached_path(current_position, board_stop, "foot"),
                "color": walk_color,
                "width": 3
            })

            # --------------------------------
            # 7️⃣ Ride the bus
            # --------------------------------

            for a, b in zip(bus_stops, bus_stops[1:]):
                segments.append({
                    "path": get_cached_path(a, b, "driving"),
                    "color": bus_color,
                    "width": 5
                })

            # Move forward in the journey
            current_position = alight_stop

        # --------------------------------
        # 8️⃣ Final walk to destination
        # --------------------------------

        segments.append({
            "path": get_cached_path(current_position, end_coords, "foot"),
            "color": walk_color,
            "width": 3
        })

        # Save this route
        all_routes.append({
            "segments": segments
        })

        # --------------------------------
        # 9️⃣ Create route button
        # --------------------------------

        if match["type"] == "transfer":
            button_text = (
                f"🔁 {buses[0]['name']} → {buses[1]['name']}"
            )
        else:
            button_text = f"🚍 {buses[0]['name']}"

        ctk.CTkButton(
            routes_panel,
            text=button_text,
            command=lambda i=route_index: show_route(i),
            anchor="w"
        ).pack(fill="x", pady=6)

# ==================================================
# Route display
# ==================================================
def show_route(index):
    """
    Draw selected route on map
    """
    global board_marker, alight_marker

    map_widget.delete_all_path()

    if board_marker:
        board_marker.delete()
    if alight_marker:
        alight_marker.delete()

    route = all_routes[index]

    # 1️⃣ Draw WALKING paths first (background)
    for segment in route["segments"]:
        if segment["width"] == 3:  # walking paths
            map_widget.set_path(
                segment["path"],
                width=segment["width"],
                color=segment["color"]
            )

    # 2️⃣ Draw BUS paths last (on top)
    for segment in route["segments"]:
        if segment["width"] == 5:  # bus paths
            map_widget.set_path(
                segment["path"],
                width=segment["width"],
                color=segment["color"]
            )

    if "board" in route:
        board_marker = map_widget.set_marker(*route["board"], text="🟢 Lên xe")
        alight_marker = map_widget.set_marker(*route["alight"], text="🔴 Xuống xe")

# ==================================================
# Start app
# ==================================================
app.mainloop()
