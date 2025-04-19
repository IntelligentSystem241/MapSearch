from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

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
  
