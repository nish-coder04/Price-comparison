from session_manager import save_cookies, load_cookies
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time, requests

DEFAULT_IMAGE = "https://placehold.co/120x120/e2e8f0/64748b?text=Product"

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def login_instamart(phone):
    print("[Instamart] Opening browser for login...")
    driver = get_driver()
    try:
        driver.get("https://www.swiggy.com/instamart")
        print("[Instamart] Please login manually in the browser window (90 seconds)...")
        time.sleep(90)
        cookies = driver.get_cookies()
        if cookies:
            save_cookies("instamart", cookies)
            print("[Instamart] Session saved for 25 days!")
    except Exception as e:
        print(f"[Instamart] Login error: {e}")
    finally:
        driver.quit()

def search_instamart(query, phone=None, pincode=None):
    cookies = load_cookies("instamart")
    if cookies:
        try:
            cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
            headers = {
                "Accept": "*/*", "Content-Type": "application/json",
                "Origin": "https://www.swiggy.com",
                "Referer": "https://www.swiggy.com/instamart/search",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Cookie": cookie_str,
            }
            url = "https://www.swiggy.com/api/instamart/search/suggest-items/v2"
            params = {
                "query": query,
                "storeId": "1402612",
                "primaryStoreId": "1402612",
                "secondaryStoreId": "",
                "trackingId": "_gjfobg8mf"
            }
            response = requests.get(url, headers=headers, params=params, timeout=10)
            print(f"[Instamart] Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                items = data.get("data", {}).get("products", [])
                if not items:
                    items = data.get("data", {}).get("items", [])
                products = []
                for item in items[:4]:
                    try:
                        name = item.get("display_name", item.get("name", ""))
                        price = float(item.get("price", item.get("selling_price", 0)))
                        if name and price > 0:
                            products.append({
                                "platform": "Instamart", "name": name,
                                "price": price,
                                "mrp": float(item.get("mrp", price)),
                                "unit": item.get("unit", item.get("quantity", "")),
                                "available": item.get("is_available", True),
                                "delivery_time": "15-20 mins",
                                "image": item.get("image_url", DEFAULT_IMAGE),
                                "logo": "🟠", "color": "#F97316", "is_live": True
                            })
                    except:
                        continue
                if products:
                    print(f"[Instamart] {len(products)} real products!")
                    return products
        except Exception as e:
            print(f"[Instamart] Error: {e}")
    print("[Instamart] Using mock data")
    from .blinkit import _mock
    return _mock(query, "Instamart", "#F97316", "🟠", "15-20 mins", price_offset=5)