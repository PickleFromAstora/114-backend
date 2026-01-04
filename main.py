print("🔥🔥🔥 RUNNING main.py 🔥🔥🔥")  # 確認程式被執行

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# ---------- 假資料 ----------
items_db = [
    {"name": "apple", "price": 10, "tax": 1},
    {"name": "banana", "price": 20, "tax": 2},
    {"name": "orange", "price": 15, "tax": 1.5},
]

# ---------- Model ----------
class Item(BaseModel):
    name: str
    price: float
    tax: Optional[float] = 0.0

# ---------- 根路由 ----------
@app.get("/")
def root():
    return {"message": "Hello world"}

@app.get("/ping")
def ping():
    return {"message": "pong"}

# ---------- 靜態路由（一定要放在動態路由前） ----------
@app.get("/items/prices")
def get_item_prices():
    return [
        {"name": item["name"], "total_price": item["price"] + item["tax"]}
        for item in items_db
    ]

@app.get("/items/names")
def get_item_names():
    return [item["name"] for item in items_db]

# ---------- 動態路由 ----------
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if 0 <= item_id < len(items_db):
        return items_db[item_id]
    return {"error": "Item not found"}

# ---------- 建立新 item ----------
@app.post("/items/")
def create_item(item: Item):
    items_db.append(item.dict())
    return item.dict()
