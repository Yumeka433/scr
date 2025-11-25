from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}

@app.get("/scrape")
def scrape(url: str):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)

        # Jika Amazon block → HTML jadi kosong
        if len(r.text) < 5000:
            return {"error": "Amazon blocked the request. Vercel IP is banned."}

        soup = BeautifulSoup(r.text, "html.parser")

        def safe(sel, attr=None):
            el = soup.select_one(sel)
            if not el: return None
            return el.get(attr) if attr else el.get_text(strip=True)

        data = {
            "title": safe("#productTitle"),
            "price": safe(".a-price .a-offscreen"),
            "image": safe("#landingImage", "src"),
            "rating": safe("i.a-icon-star span"),
            "url": url
        }

        return data

    except Exception as e:
        # Supaya Vercel tidak 404 → kita balikan error JSON
        return {"error": str(e)}


@app.get("/")
def root():
    return {"status": "API OK"}
