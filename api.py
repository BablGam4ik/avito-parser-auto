import json
import os
from typing import Optional, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    city: str
    max_price: Optional[int] = None


@app.get("/")
async def root():
    return {"status": "ok", "endpoints": {"/health": "GET", "/search": "POST"}}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/search")
async def search(request: SearchRequest):
    # Демо-данные для всех городов
    demo_apartments = {
        "москва": [
            {"id": 1, "title": "Квартира на Патриарших", "price": 8900, "address": "Москва, Патриаршая, 12",
             "city": "Москва"},
            {"id": 2, "title": "Апартаменты Арбат", "price": 12500, "address": "Москва, Арбат, 8", "city": "Москва"},
            {"id": 3, "title": "ВДНХ Дизайн", "price": 9900, "address": "Москва, пр-т Мира, 150", "city": "Москва"},
        ],
        "сочи": [
            {"id": 4, "title": "Студия у моря", "price": 5200, "address": "Сочи, Приморская, 5", "city": "Сочи"},
            {"id": 5, "title": "Адлер у парка", "price": 6100, "address": "Сочи, ул. Ленина, 30", "city": "Сочи"},
        ],
        "санкт-петербург": [
            {"id": 6, "title": "Невский простор", "price": 7100, "address": "Санкт-Петербург, Невский пр., 88",
             "city": "Санкт-Петербург"},
            {"id": 7, "title": "Квартира у Канала", "price": 8300,
             "address": "Санкт-Петербург, наб. Канала Грибоедова, 45", "city": "Санкт-Петербург"},
        ],
        "казань": [
            {"id": 8, "title": "Казань Центр", "price": 4900, "address": "Казань, ул. Баумана, 25", "city": "Казань"},
        ]
    }

    city_lower = request.city.lower()
    apartments = demo_apartments.get(city_lower, [])

    return {
        "success": True,
        "count": len(apartments),
        "apartments": apartments
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)