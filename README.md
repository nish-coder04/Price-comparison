# 🛒 QuickCompare — Smart Price Comparison Tool

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20App-black?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite)
![Selenium](https://img.shields.io/badge/Selenium-Scraping-green?logo=selenium)
![License](https://img.shields.io/badge/License-MIT-yellow)

A web-based price comparison tool that scrapes real-time grocery prices across **Blinkit, Zepto, and Instamart** — helping users find the cheapest deal instantly.

---

## ✨ Features

- 🔍 **Live Price Comparison** — search any product and compare prices across 3 platforms
- 🗄️ **Price History** — stores data in a local SQLite database for trend tracking
- 🔐 **Login & Session Management** — user authentication with session handling
- ⚙️ **Modular Scrapers** — separate scraper modules for each platform
- 🌐 **Clean Web UI** — simple Flask-based frontend

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.x | Core language |
| Flask | Web framework |
| SQLite | Local price database |
| Selenium | Web scraping (Blinkit, Zepto, Instamart) |
| HTML/CSS | Frontend interface |

---

## 📁 Project Structure

```
Price-comparison/
├── app.py                 # Flask app & routes
├── database.py            # DB setup & queries
├── login.py               # Authentication logic
├── session_manager.py     # Session handling
├── __init__.py            # Package init
├── scrapers/              # Platform-specific scrapers
│   ├── blinkit.py
│   ├── zepto.py
│   └── instamart.py
├── templates/             # HTML templates
├── requirements.txt       # Dependencies
└── settings.example.json  # Config template
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Google Chrome + ChromeDriver (for Selenium)
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/nish-coder04/Price-comparison.git
cd Price-comparison
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup configuration**
```bash
cp settings.example.json settings.json
# Edit settings.json with your credentials
```

4. **Run the app**
```bash
python app.py
```

5. **Open in browser**
http://127.0.0.1:5000

---

## ⚠️ Note

This tool uses Selenium to scrape live prices. Make sure **ChromeDriver version matches your installed Chrome browser**. Scraping behavior may vary based on platform UI changes.

---

## 👩‍💻 Author

**Nishtha Shukla** — AI/ML Engineer  
🌐 [Portfolio](https://nishtha-ns.vercel.app) | 💼 [LinkedIn](https://www.linkedin.com/in/nishtha-shukla-ns)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
