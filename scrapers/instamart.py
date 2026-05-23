import requests
from .blinkit import _mock

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

def search_instamart(query, lat="28.6139", lon="77.2090"):
    try:
        url = "https://www.swiggy.com/api/instamart/search"
        params = {"query": query, "pageNumber": 0, "pageSize": 5, "lat": lat, "lng": lon}
        response = requests.get(url, params=params, headers=HEADERS, timeout=8)
        if response.status_code == 200:
            data = response.json()
            products = []
            for item in data.get("data", {}).get("products", [])[:3]:
                products.append({
                    "platform": "Instamart",
                    "name": item.get("name", ""),
                    "price": float(item.get("price", 0)),
                    "mrp": float(item.get("mrp", 0)),
                    "unit": item.get("quantity", ""),
                    "available": item.get("inStock", True),
                    "delivery_time": "15-20 mins",
                    "image": item.get("imageId", ""),
                    "logo": "🟠", "color": "#F97316",
                    "is_live": True
                })
            if products:
                return products
    except Exception as e:
        print(f"[Instamart] Live fetch failed — using mock data")
    # Instamart prices are slightly higher
    return _mock(query, "Instamart", "#F97316", "🟠", "15-20 mins", price_offset=5)
