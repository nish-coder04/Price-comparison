import json
import os
from datetime import datetime, timedelta

SESSIONS_DIR = "sessions"

def ensure_dir():
    if not os.path.exists(SESSIONS_DIR):
        os.makedirs(SESSIONS_DIR)

def save_cookies(platform, cookies):
    ensure_dir()
    data = {
        "cookies": cookies,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "expires_at": (datetime.now() + timedelta(days=25)).strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(f"{SESSIONS_DIR}/{platform}.json", "w") as f:
        json.dump(data, f)
    print(f"[{platform}] Session saved! Valid for 25 days.")

def load_cookies(platform):
    ensure_dir()
    path = f"{SESSIONS_DIR}/{platform}.json"
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        data = json.load(f)
    expires = datetime.strptime(data["expires_at"], "%Y-%m-%d %H:%M:%S")
    if datetime.now() > expires:
        print(f"[{platform}] Session expired! Need to login again.")
        os.remove(path)
        return None
    print(f"[{platform}] Using saved session (expires {data['expires_at']})")
    return data["cookies"]

def session_exists(platform):
    path = f"{SESSIONS_DIR}/{platform}.json"
    if not os.path.exists(path):
        return False
    with open(path, "r") as f:
        data = json.load(f)
    expires = datetime.strptime(data["expires_at"], "%Y-%m-%d %H:%M:%S")
    return datetime.now() < expires

def session_status():
    status = {}
    for platform in ["blinkit", "zepto", "instamart"]:
        path = f"{SESSIONS_DIR}/{platform}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
            expires = datetime.strptime(data["expires_at"], "%Y-%m-%d %H:%M:%S")
            if datetime.now() < expires:
                days_left = (expires - datetime.now()).days
                status[platform] = {"active": True, "days_left": days_left}
            else:
                status[platform] = {"active": False, "days_left": 0}
        else:
            status[platform] = {"active": False, "days_left": 0}
    return status