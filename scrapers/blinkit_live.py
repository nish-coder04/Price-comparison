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

def login_blinkit(phone):
    print("[Blinkit] Opening browser for login...")
    driver = get_driver()
    try:
        driver.get("https://blinkit.com")
        print("[Blinkit] Please login manually in the browser window (90 seconds)...")
        time.sleep(90)
        cookies = driver.get_cookies()
        if cookies:
            save_cookies("blinkit", cookies)
            print("[Blinkit] Session saved for 25 days!")
    except Exception as e:
        print(f"[Blinkit] Login error: {e}")
    finally:
        driver.quit()

def search_blinkit(query, phone=None, pincode=None):
    cookies = load_cookies("blinkit")
    if cookies:
        try:
            cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
                "App_client": "consumer_web",
                "App_version": "1010101010",
                "lat": "26.8009672", "lon": "75.8685903",
                "Cookie": cookie_str,
            }
            url = "https://blinkit.com/v6/search/products"
            params = {"start": 0, "size": 10, "search_type": 3, "q": query,
                      "lat": "26.8009672", "lon": "75.8685903"}
            response = requests.get(url, params=params, headers=headers, timeout=10)
            print(f"[Blinkit] Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                items = data.get("objects", {}).get("products", [])
                products = []
                for item in items[:4]:
                    name = item.get("name", "")
                    price = float(item.get("price", 0))
                    if name and price > 0:
                        products.append({
                            "platform": "Blinkit", "name": name, "price": price,
                            "mrp": float(item.get("mrp", price)),
                            "unit": item.get("unit", ""),
                            "available": bool(item.get("in_stock", 1)),
                            "delivery_time": "8 mins",
                            "image": item.get("image", DEFAULT_IMAGE),
                            "logo": "🟡", "color": "#F8D146", "is_live": True
                        })
                if products:
                    print(f"[Blinkit] {len(products)} real products!")
                    return products
        except Exception as e:
            print(f"[Blinkit] Error: {e}")
    print("[Blinkit] Using mock data")
    from .blinkit import _mock
    return _mock(query, "Blinkit", "#F8D146", "🟡", "8 mins", price_offset=0)