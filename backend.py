import sqlite3, json, joblib, numpy as np, pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sklearn.metrics import pairwise_distances
from pathlib import Path

# === Paths ===
ART_DIR = Path("artifacts")
DB = "telecom.db"
PLANS_FILE = ART_DIR / "plan_catalog.csv"
FEATURES_FILE = ART_DIR / "features.json"
SCALER_FILE = ART_DIR / "scaler.pkl"
KMEANS_FILE = ART_DIR / "kmeans.pkl"

# === Flask app ===
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# === Load model + features ===
try:
    scaler = joblib.load(SCALER_FILE)
    kmeans = joblib.load(KMEANS_FILE)
    with open(FEATURES_FILE) as f:
        feat_names = json.load(f)
    plans_df = pd.read_csv(PLANS_FILE)
except Exception as e:
    print(f"Error loading model artifacts: {e}")
    raise

def db_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def parse_centroid_text(s):
    try: return json.loads(s)
    except: import ast; return ast.literal_eval(s)

def recommend_top3(payload):
    vec = []
    for f in feat_names:
        if f == "Total_Usage":
            total = sum(float(payload.get(c, 0)) for c in ["Day Mins", "Eve Mins", "Night Mins", "Intl Mins"])
            vec.append(total)
        else:
            vec.append(float(payload.get(f, 0)))

    x = np.array(vec).reshape(1, -1)
    x_scaled = scaler.transform(x)
    dists = pairwise_distances(x_scaled, kmeans.cluster_centers_, metric="euclidean")[0]
    top_idx = np.argsort(dists)[:3]

    recs = []
    for idx in top_idx:
        # Use the pre-loaded pandas DataFrame to find the row
        row = plans_df[plans_df["plan_id"] == idx].iloc[0]
        recs.append({
            "plan_id": int(row["plan_id"]),
            "name": row["name"],
            "price": float(row["price"]),
            "distance": float(dists[idx]),
            "centroid": parse_centroid_text(row["centroid"])
        })
    return recs

# === Routes ===
@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    phone = data.get("phone")
    conn = db_conn()
    cust = conn.execute("SELECT * FROM customers WHERE phone=?", (phone,)).fetchone()
    if not cust:
        conn.close()
        return jsonify({"error": "Phone not found"}), 404

    # The current_plan field is not provided in your backend response,
    # so I've added a lookup here to fetch the plan details.
    plan = conn.execute("SELECT * FROM plans WHERE plan_id=?", (cust["current_plan_id"],)).fetchone()
    conn.close()

    usage = {
        "Day Mins": cust["day_mins"],
        "Eve Mins": cust["eve_mins"],
        "Night Mins": cust["night_mins"],
        "Intl Mins": cust["intl_mins"],
        "CustServ Calls": cust["custserv_calls"]
    }

    recs = recommend_top3(usage)
    return jsonify({
        "phone": phone,
        "current_plan": dict(plan),
        "recommendations": recs
    })

@app.route("/api/predict", methods=["POST"])
def api_predict():
    payload = request.json
    recs = recommend_top3(payload)
    return jsonify({"recommendations": recs})

@app.route("/api/plans", methods=["GET"])
def api_get_all_plans():
    conn = db_conn()
    plans = conn.execute("SELECT plan_id, name, price, centroid FROM plans ORDER BY plan_id").fetchall()
    conn.close()
    return jsonify({
        "plans": [dict(plan) for plan in plans]
    })

# === Run server ===
if __name__ == "__main__":
    app.run(port=5001, debug=True)
