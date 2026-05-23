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

def login_zepto(phone):
    print("[Zepto] Opening browser for login...")
    driver = get_driver()
    try:
        driver.get("https://zepto.in/search")
        print("[Zepto] Please login manually in the browser window (90 seconds)...")
        time.sleep(90)
        cookies = driver.get_cookies()
        if cookies:
            save_cookies("zepto", cookies)
            print("[Zepto] Session saved for 25 days!")
    except Exception as e:
        print(f"[Zepto] Login error: {e}")
    finally:
        driver.quit()

def search_zepto(query, phone=None, pincode=None):
    cookies = load_cookies("zepto")
    if cookies:
        try:
            cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
            store_id = "b4dc8d65-ed2e-4142-81b6-373982b13500"
            headers = {
                "Accept": "application/json, text/plain, */*",
                "App_sub_platform": "WEB", "App_version": "15.17.5",
                "Appversion": "15.17.5", "Auth_from_cookie": "true",
                "Auth_revamp_flow": "v2", "Content-Type": "application/json",
                "Origin": "https://www.zepto.in", "Referer": "https://www.zepto.in/",
                "Store_id": store_id, "Storeid": store_id, "Tenant": "ZEPTO",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Cookie": cookie_str,
            }
            payload = {"query": query, "pageNumber": 0, "mode": "TYPED"}
            url = "https://bff-gateway.zepto.com/user-search-service/api/v3/search"
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            print(f"[Zepto] Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                sections = data.get("data", {}).get("sections", [])
                items = []
                for section in sections:
                    for item in section.get("items", []):
                        product = item.get("productResponse", {})
                        if product:
                            items.append(product)
                products = []
                for item in items[:4]:
                    try:
                        name = item.get("name", "")
                        price_raw = float(item.get("discountedPrice", item.get("mrpPrice", 0)))
                        price = price_raw / 100 if price_raw > 500 else price_raw
                        mrp_raw = float(item.get("mrpPrice", price_raw))
                        mrp = mrp_raw / 100 if mrp_raw > 500 else mrp_raw
                        if name and price > 0:
                            products.append({
                                "platform": "Zepto", "name": name,
                                "price": price, "mrp": mrp,
                                "unit": item.get("unitString", ""),
                                "available": not item.get("outOfStock", False),
                                "delivery_time": "10 mins",
                                "image": item.get("imgUrl", DEFAULT_IMAGE),
                                "logo": "🟣", "color": "#8B5CF6", "is_live": True
                            })
                    except:
                        continue
                if products:
                    print(f"[Zepto] {len(products)} real products!")
                    return products
        except Exception as e:
            print(f"[Zepto] Error: {e}")
    print("[Zepto] Using mock data")
    from .blinkit import _mock
    return _mock(query, "Zepto", "#8B5CF6", "🟣", "10 mins", price_offset=-3)