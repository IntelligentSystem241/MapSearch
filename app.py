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
  @app.route("/send_sms", methods=["POST"])
def send_sms():
    data = request.get_json()
    phone = data.get("phone")
    message = data.get("message")

    try:
        api = SpeedSMSAPI("VSwbgZoWdyz3C3N9AiHJfaEReP0wWuYV")  # <-- nhập token SpeedSMS ở đây
        result = api.send_sms(phone, message, 5, "c660f859b35d5493") 
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
