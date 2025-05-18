from flask import Flask, render_template, request, jsonify
import time
import requests

app = Flask(__name__)

def seconds_since_epoch():
    epoch = time.time()
    return int(epoch)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/seconds")
def seconds():
    return str(seconds_since_epoch())

@app.route("/minutes")
def minutes():
    return str(seconds_since_epoch() // 60)

@app.route("/hours")
def hours():
    return str(seconds_since_epoch() // 3600)

@app.route("/map")
def map_view():
    return render_template("map.html")

@app.route("/elevation")
def elevation():
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    # Try OpenTopodata SRTM90m first
    try:
        resp = requests.get(f'https://api.opentopodata.org/v1/srtm90m?locations={lat},{lng}', timeout=5)
        data = resp.json()
        if data and 'results' in data and data['results'][0]['elevation'] is not None:
            return jsonify(data)
    except Exception:
        pass
    # Fallback to Open-Elevation
    try:
        resp = requests.get(f'https://api.open-elevation.com/api/v1/lookup?locations={lat},{lng}', timeout=5)
        data = resp.json()
        if data and 'results' in data and data['results'][0]['elevation'] is not None:
            return jsonify(data)
    except Exception:
        pass
    # If all fail, return N/A
    return jsonify({"results": [{"elevation": None}]})

