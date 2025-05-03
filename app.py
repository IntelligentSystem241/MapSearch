from flask import Flask, request, jsonify, render_template
import requests
import pandas as pd
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__)

# --- Tính khoảng cách Haversine ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # bán kính trái đất (km)
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

# --- Tìm bão trong vùng bán kính ---
def find_storms_near(lat_user, lon_user, radius_km=1000):
    url = "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/access/csv/IBTrACS.last3years.list.v04r00.csv"
    df = pd.read_csv(url, skiprows=1)
    df = df[['SID', 'Name', 'Latitude', 'Longitude', 'ISO_TIME']].dropna()

    df['Distance_km'] = df.apply(lambda row: haversine(lat_user, lon_user, row['Latitude'], row['Longitude']), axis=1)
    nearby = df[df['Distance_km'] <= radius_km]
    result = nearby.groupby('SID').first().reset_index()
    result = result[['SID', 'Name', 'ISO_TIME', 'Distance_km']].sort_values('Distance_km')
    return result.to_dict(orient="records")

@app.route("/")
def index():
    return render_template("map.html")

@app.route("/get_coords", methods=["POST"])
def get_coords():
    data = request.get_json()
    address = data.get("address")
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": "MyMapApp/1.0 (your-email@example.com)"}
    
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200 and response.json():
        result = response.json()[0]
        return jsonify({"lat": result["lat"], "lon": result["lon"]})
    return jsonify({"error": "Không tìm thấy tọa độ"}), 404

@app.route("/check_storms", methods=["POST"])
def check_storms():
    data = request.get_json()
    lat = float(data.get("lat"))
    lon = float(data.get("lon"))
    storms = find_storms_near(lat, lon)
    return jsonify(storms=storms)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
