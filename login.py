from scrapers.blinkit_live import login_blinkit
from scrapers.zepto_live import login_zepto
from scrapers.instamart_live import login_instamart
from session_manager import session_status

print("=" * 50)
print("  QuickCompare — One-Time Login Setup")
print("=" * 50)

status = session_status()
print("\n Current Session Status:")
for platform, info in status.items():
    if info["active"]:
        print(f"  {platform.title()} — Active ({info['days_left']} days left)")
    else:
        print(f"  {platform.title()} — Not logged in")

print("\nWhich platform do you want to login to?")
print("1. Blinkit")
print("2. Zepto")
print("3. Instamart")
print("4. All 3 platforms")
print("5. Exit")

choice = input("\nEnter choice (1-5): ").strip()

phone = ""
if choice in ["1", "2", "3", "4"]:
    phone = input("Enter your phone number: ").strip()

if choice == "1":
    login_blinkit(phone)
elif choice == "2":
    login_zepto(phone)
elif choice == "3":
    login_instamart(phone)
elif choice == "4":
    print("\n Logging into all 3 platforms...")
    login_blinkit(phone)
    login_zepto(phone)
    login_instamart(phone)
    print("\n All platforms logged in!")
elif choice == "5":
    print("Exiting...")

print("\n Updated Session Status:")
status = session_status()
for platform, info in status.items():
    if info["active"]:
        print(f"  {platform.title()} — Active ({info['days_left']} days left)")
    else:
        print(f"  {platform.title()} — Not logged in")

print("\nNow run: python app.py")