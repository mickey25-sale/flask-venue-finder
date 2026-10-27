from flask import Flask, render_template, jsonify
from flask import Flask, render_template
import requests
import csv
import io

app = Flask(__name__)

# Your published Google Sheet
SHEET_CSV_URL ="https://docs.google.com/spreadsheets/d/e/2PACX-1vROiTq-W_OdNM2ZoWur6yJFHOOYaMBxMxis4cybVBH6YPeNdpRzjpe2GGjHxk_ziAOTs4iGF7k3Ajpz/pub?gid=0&single=true&output=csv"

@app.route("/")
def home():
    try:
        # Download the latest published sheet data
        response = requests.get(SHEET_CSV_URL, timeout=15)
        response.raise_for_status()

        # Convert CSV data into Python dictionaries
        reader = csv.DictReader(io.StringIO(response.text))
        venues = list(reader)

        error = None

    except requests.RequestException:
        venues = []
        error = "Could not load venues. Check your internet connection and published sheet."

    return render_template(
        "index.html",
        venues=venues,
        error=error
    )

@app.route("/api/venues")
def api_venues():
    print("API ROUTE CALLED")

    try:
        print("FETCHING GOOGLE SHEETS...")

        response = requests.get(SHEET_CSV_URL, timeout=15)

        print("HTTP STATUS:", response.status_code)
        print("RESPONSE PREVIEW:", response.text[:200])

        response.raise_for_status()

        reader = csv.DictReader(io.StringIO(response.text))
        venues = list(reader)

        print("VENUES FOUND:", len(venues))

        return jsonify({"venues": venues})

    except requests.RequestException as e:
        print("GOOGLE SHEETS ERROR:", repr(e))
        return jsonify({"error": "Could not load venues"}), 502
if __name__ == "__main__":
    app.run(debug=True)