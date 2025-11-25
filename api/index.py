from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/scrape")   # ❗ ini penting, JANGAN tulis /api/scrape
def scrape(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.select_one("#productTitle")
    price = soup.select_one(".a-price .a-offscreen")
    image = soup.select_one("#landingImage")
    rating = soup.select_one("i.a-icon-star span")

    return {
        "title": title.get_text(strip=True) if title else None,
        "price": price.get_text(strip=True) if price else None,
        "image": image.get("src") if image else None,
        "rating": rating.get_text(strip=True) if rating else None,
        "url": url
    }

@app.get("/")
def root():
    return {"status": "API is running"}
