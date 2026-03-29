import json
import requests

# your local OSRM server
OSRM_URL = "http://localhost:6969/route/v1/driving"

OUTPUT_FILE = "precomputed_routes.json"

# import your bus data
from bus_routes import BUS_AND_METRO_ROUTES   # <-- make sure this exists


def format_coord(coord):
    return f"{coord[0]:.6f},{coord[1]:.6f}"


def get_osrm_path(a, b):
    url = f"{OSRM_URL}/{a[1]},{a[0]};{b[1]},{b[0]}?overview=full&geometries=geojson"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        coords = response.json()["routes"][0]["geometry"]["coordinates"]

        # convert (lon, lat) → (lat, lon)
        return [(lat, lon) for lon, lat in coords]

    except Exception as e:
        print(f"❌ Failed: {a} → {b} | {e}")
        return None


def main():
    precomputed = {}
    total = 0

    for route in BUS_AND_METRO_ROUTES:
        stops = route["coords"]   # IMPORTANT: must be "coords"

        for i in range(len(stops) - 1):
            a = stops[i]
            b = stops[i + 1]

            key = f"{format_coord(a)}-{format_coord(b)}"

            # skip if already computed
            if key in precomputed:
                continue

            print(f"Computing {total}: {key}")

            path = get_osrm_path(a, b)

            if path:
                precomputed[key] = path
                total += 1

    # save to file
    with open(OUTPUT_FILE, "w") as f:
        json.dump(precomputed, f)

    print(f"\n✅ Done. Saved {total} segments to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()