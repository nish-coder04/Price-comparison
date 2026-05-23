import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-IN,en-US;q=0.9",
    "app_client": "consumer",
    "web_app_version": "1000",
}

DEFAULT_IMAGE = "https://placehold.co/120x120/e2e8f0/64748b?text=Product"

MOCK_DB = {
    "milk": [
        {"name": "Amul Full Cream Milk", "price": 66, "mrp": 68, "unit": "1L", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Milk_glass.jpg/240px-Milk_glass.jpg"},
        {"name": "Mother Dairy Toned Milk", "price": 58, "mrp": 60, "unit": "500ml", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Milk_glass.jpg/240px-Milk_glass.jpg"},
    ],
    "bread": [
        {"name": "Britannia Brown Bread", "price": 40, "mrp": 44, "unit": "400g", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_bread_05.jpg/240px-Fresh_made_bread_05.jpg"},
        {"name": "Modern White Sandwich Bread", "price": 35, "mrp": 38, "unit": "400g", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_bread_05.jpg/240px-Fresh_made_bread_05.jpg"},
    ],
    "eggs": [
        {"name": "Farm Fresh White Eggs", "price": 84, "mrp": 90, "unit": "12 pcs", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Chicken_egg_2009.jpg/240px-Chicken_egg_2009.jpg"},
    ],
    "rice": [
        {"name": "India Gate Basmati Rice", "price": 149, "mrp": 160, "unit": "1kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/White_rice.jpg/240px-White_rice.jpg"},
        {"name": "Fortune Basmati Rice", "price": 135, "mrp": 145, "unit": "1kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/White_rice.jpg/240px-White_rice.jpg"},
    ],
    "sugar": [
        {"name": "Tata Sugar Refined", "price": 45, "mrp": 50, "unit": "1kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Raw_sugar_80b.jpg/240px-Raw_sugar_80b.jpg"},
    ],
    "onion": [
        {"name": "Fresh Onion", "price": 35, "mrp": 40, "unit": "1kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Onions.jpg/240px-Onions.jpg"},
    ],
    "tomato": [
        {"name": "Fresh Tomato", "price": 30, "mrp": 35, "unit": "500g", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Tomato_je.jpg/240px-Tomato_je.jpg"},
    ],
    "butter": [
        {"name": "Amul Butter", "price": 55, "mrp": 58, "unit": "100g", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Butter_dish.jpg/240px-Butter_dish.jpg"},
    ],
    "chips": [
        {"name": "Lay's Classic Salted", "price": 20, "mrp": 20, "unit": "26g", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Potato_chips_bag.jpg/240px-Potato_chips_bag.jpg"},
        {"name": "Kurkure Masala Munch", "price": 20, "mrp": 20, "unit": "90g", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Potato_chips_bag.jpg/240px-Potato_chips_bag.jpg"},
    ],
    "cold drink": [
        {"name": "Coca Cola", "price": 40, "mrp": 45, "unit": "750ml", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Coca-Cola_bottle_cap.svg/240px-Coca-Cola_bottle_cap.svg.png"},
        {"name": "Pepsi", "price": 38, "mrp": 42, "unit": "750ml", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Coca-Cola_bottle_cap.svg/240px-Coca-Cola_bottle_cap.svg.png"},
    ],
    "biscuit": [
        {"name": "Parle-G Gold Biscuits", "price": 10, "mrp": 10, "unit": "100g", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Biscuit_cookies.jpg/240px-Biscuit_cookies.jpg"},
        {"name": "Britannia Good Day Butter", "price": 35, "mrp": 38, "unit": "200g", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Biscuit_cookies.jpg/240px-Biscuit_cookies.jpg"},
    ],
    "atta": [
        {"name": "Aashirvaad Whole Wheat Atta", "price": 280, "mrp": 295, "unit": "5kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Wheat_flour_in_bowl.jpg/240px-Wheat_flour_in_bowl.jpg"},
    ],
    "banana": [
        {"name": "Fresh Banana", "price": 49, "mrp": 55, "unit": "12 pcs", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Banana-Bananas.jpg/240px-Banana-Bananas.jpg"},
    ],
    "apple": [
        {"name": "Fresh Apple Shimla", "price": 149, "mrp": 160, "unit": "1kg", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Red_Apple.jpg/240px-Red_Apple.jpg"},
    ],
    "chocolate": [
        {"name": "Dairy Milk Silk", "price": 99, "mrp": 105, "unit": "145g", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Chocolate_bar.jpg/240px-Chocolate_bar.jpg"},
        {"name": "KitKat Chocolate", "price": 40, "mrp": 42, "unit": "41.5g", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Chocolate_bar.jpg/240px-Chocolate_bar.jpg"},
    ],
    "maggi": [
        {"name": "Maggi 2-Minute Noodles", "price": 14, "mrp": 14, "unit": "70g", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Noodles_mixed_spicy_south_korea.jpg/240px-Noodles_mixed_spicy_south_korea.jpg"},
    ],
    "oil": [
        {"name": "Fortune Sunflower Oil", "price": 155, "mrp": 165, "unit": "1L", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Cooking_oil.jpg/240px-Cooking_oil.jpg"},
        {"name": "Saffola Gold Oil", "price": 175, "mrp": 185, "unit": "1L", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Cooking_oil.jpg/240px-Cooking_oil.jpg"},
    ],
}

def _mock(query, platform, color, logo, delivery, price_offset=0):
    key = next((k for k in MOCK_DB if k in query.lower()), None)
    items = MOCK_DB.get(key, [{"name": query.title(), "price": 99, "mrp": 110, "unit": "1 pc", "image": DEFAULT_IMAGE}])
    return [{
        "platform": platform,
        "name": i["name"],
        "price": round(i["price"] + price_offset, 2),
        "mrp": i["mrp"],
        "unit": i["unit"],
        "available": True,
        "delivery_time": delivery,
        "image": i.get("image", DEFAULT_IMAGE),
        "logo": logo,
        "color": color,
        "is_live": False
    } for i in items]

def search_blinkit(query, lat="28.6139", lon="77.2090"):
    try:
        url = "https://blinkit.com/v6/search/products"
        params = {"start": 0, "size": 5, "search_type": 3, "q": query, "lat": lat, "lon": lon}
        session = requests.Session()
        session.headers.update(HEADERS)
        session.get("https://blinkit.com", timeout=5)
        response = session.get(url, params=params, timeout=8)
        if response.status_code == 200:
            data = response.json()
            products = []
            for item in data.get("objects", {}).get("products", [])[:3]:
                products.append({
                    "platform": "Blinkit",
                    "name": item.get("name", ""),
                    "price": float(item.get("price", 0)),
                    "mrp": float(item.get("mrp", item.get("price", 0))),
                    "unit": item.get("unit", ""),
                    "available": bool(item.get("in_stock", 1)),
                    "delivery_time": "10 mins",
                    "image": item.get("image", DEFAULT_IMAGE),
                    "logo": "🟡", "color": "#F8D146",
                    "is_live": True
                })
            if products:
                return products
    except Exception as e:
        print(f"[Blinkit] Live fetch failed — using mock data")
    return _mock(query, "Blinkit", "#F8D146", "🟡", "10 mins", price_offset=0)