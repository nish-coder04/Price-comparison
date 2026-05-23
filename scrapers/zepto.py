import requests
from .blinkit import _mock

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

def search_zepto(query, lat="28.6139", lon="77.2090"):
    try:
        url = "https://api.zepto.in/v1/search"
        params = {"query": query, "page": 1, "limit": 5}
        response = requests.get(url, params=params, headers=HEADERS, timeout=8)
        if response.status_code == 200:
            data = response.json()
            products = []
            for item in data.get("data", {}).get("products", [])[:3]:
                products.append({
                    "platform": "Zepto",
                    "name": item.get("name", ""),
                    "price": float(item.get("discountedPrice", 0) / 100),
                    "mrp": float(item.get("mrp", 0) / 100),
                    "unit": item.get("unitStr", ""),
                    "available": not item.get("outOfStock", False),
                    "delivery_time": "10 mins",
                    "image": item.get("imgUrl", ""),
                    "logo": "🟣", "color": "#8B5CF6",
                    "is_live": True
                })
            if products:
                return products
    except Exception as e:
        print(f"[Zepto] Live fetch failed — using mock data")
    # Zepto prices are slightly different (±5)
    return _mock(query, "Zepto", "#8B5CF6", "🟣", "10 mins", price_offset=-3)
