print("🔥🔥🔥 FASTAPI APP LOADED 🔥🔥🔥")

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# --------------------
# 假資料庫
# --------------------
fake_items_db = [
    {"name": "apple", "price": 10.0, "tax": 1.0},
    {"name": "banana", "price": 20.0, "tax": 2.0},
    {"name": "orange", "price": 15.0, "tax": 1.5},
]

# --------------------
# Model
# --------------------
class Item(BaseModel):
    name: str = Field(..., example="apple")
    price: float = Field(..., gt=0)
    tax: Optional[float] = 0.0

# --------------------
# 基本測試
# --------------------
@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/ping")
def ping():
    return {"message": "pong"}

# --------------------
# 靜態路由（一定要放前面）
# --------------------
@app.get("/items/names")
def get_item_names():
    return [item["name"] for item in fake_items_db]

@app.get("/items/prices")
def get_item_prices():
    return [
        {
            "name": item["name"],
            "total_price": item["price"] + item["tax"]
        }
        for item in fake_items_db
    ]

@app.get("/items/stats")
def get_item_stats():
    prices = [item["price"] for item in fake_items_db]
    return {
        "count": len(prices),
        "total": sum(prices),
        "average": sum(prices) / len(prices) if prices else 0,
        "max": max(prices) if prices else 0,
        "min": min(prices) if prices else 0,
    }

@app.get("/items/search")
def search_items(keyword: str = Query(..., min_length=1)):
    return [
        item for item in fake_items_db
        if keyword.lower() in item["name"].lower()
    ]

# --------------------
# 動態路由
# --------------------
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

@app.get("/items/{item_id}")
def read_item(item_id: int = Path(..., ge=0)):
    if item_id >= len(fake_items_db):
        return {"error": "Item not found"}
    return fake_items_db[item_id]

@app.post("/items/")
def create_item(item: Item):
    fake_items_db.append(item.model_dump())
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id >= len(fake_items_db):
        return {"error": "Item not found"}
    fake_items_db[item_id] = item.model_dump()
    return fake_items_db[item_id]

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id >= len(fake_items_db):
        return {"error": "Item not found"}
    deleted = fake_items_db.pop(item_id)
    return {"deleted": deleted}
