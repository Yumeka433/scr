from fastapi import FastAPI, Query
import httpx

app = FastAPI()

GOOGLE_BOOKS = "https://www.googleapis.com/books/v1/volumes"

@app.get("/api/books")
async def search_books(q: str = Query(...)):
    async with httpx.AsyncClient() as client:
        r = await client.get(GOOGLE_BOOKS, params={"q": q, "maxResults": 5})

    data = r.json()

    if "items" not in data:
        return {"books": []}

    books = []

    for item in data["items"]:
        info = item.get("volumeInfo", {})
        access = item.get("accessInfo", {})

        books.append({
            "title": info.get("title"),
            "authors": info.get("authors"),
            "publisher": info.get("publisher"),
            "publishedDate": info.get("publishedDate"),
            "description": info.get("description"),
            "thumbnail": info.get("imageLinks", {}).get("thumbnail"),
            "download_links": {
                "pdf": access.get("pdf", {}).get("downloadLink"),
                "epub": access.get("epub", {}).get("downloadLink"),
            }
        })

    return {"books": books}
