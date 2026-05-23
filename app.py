from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
from database import init_db, save_price, get_price_history
import json, os

app = Flask(__name__)
app.secret_key = "quickcompare_secret_2024"
CORS(app)
init_db()

SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"phone": "", "pincode": "", "use_live": False}

def save_settings_to_file(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f)

def fetch_all(query, phone, pincode, use_live):
    if use_live and phone and pincode:
        try:
            from scrapers.blinkit_live import search_blinkit
            from scrapers.zepto_live import search_zepto
            from scrapers.instamart_live import search_instamart
            print(f"[LIVE] Fetching real prices for '{query}'...")
            b = search_blinkit(query, phone, pincode)
            z = search_zepto(query, phone, pincode)
            i = search_instamart(query, phone, pincode)
            return b + z + i
        except Exception as e:
            print(f"[LIVE] Error: {e} — using mock data")

    from scrapers.blinkit import search_blinkit
    from scrapers.zepto import search_zepto
    from scrapers.instamart import search_instamart
    with ThreadPoolExecutor(max_workers=3) as executor:
        b = executor.submit(search_blinkit, query)
        z = executor.submit(search_zepto, query)
        i = executor.submit(search_instamart, query)
        return b.result() + z.result() + i.result()

@app.route("/")
def index():
    settings = load_settings()
    return render_template("index.html", settings=settings)

@app.route("/settings", methods=["GET", "POST"])
def settings_route():
    if request.method == "POST":
        data = request.get_json()
        save_settings_to_file({
            "phone": data.get("phone", ""),
            "pincode": data.get("pincode", ""),
            "use_live": data.get("use_live", False)
        })
        return jsonify({"success": True})
    return jsonify(load_settings())

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Please enter a product name"}), 400

    s = load_settings()
    results = fetch_all(query, s.get("phone",""), s.get("pincode",""), s.get("use_live", False))

    for p in results:
        save_price(query, p["platform"], p["price"], p.get("unit",""), p.get("available", True), p.get("delivery_time",""))

    available = [r for r in results if r.get("available", True)]
    best_deal = min(available, key=lambda x: x["price"]) if available else None

    by_platform = {}
    for r in results:
        by_platform.setdefault(r["platform"], []).append(r)
    for p in by_platform:
        by_platform[p].sort(key=lambda x: x["price"])

    prices = [r["price"] for r in available]
    max_saving = round(max(prices) - min(prices), 2) if len(prices) >= 2 else 0
    is_live = any(r.get("is_live", False) for r in results)

    return jsonify({
        "query": query,
        "results": results,
        "by_platform": by_platform,
        "best_deal": best_deal,
        "total_products": len(results),
        "max_saving": max_saving,
        "is_live": is_live,
        "pincode": s.get("pincode", "")
    })

@app.route("/history")
def history():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "No query"}), 400
    return jsonify({"query": query, "history": get_price_history(query)})

if __name__ == "__main__":
    print("🚀 Starting Quick Commerce Price Comparator...")
    print("📦 Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)