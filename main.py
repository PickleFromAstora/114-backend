from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field

app = FastAPI()

# ----------------------------
# 假資料庫
# ----------------------------
items_db = [
    {"name": "apple", "price": 10.0, "tax": 1.0},
    {"name": "banana", "price": 20.0, "tax": 2.0},
    {"name": "orange", "price": 15.0, "tax": 1.5},
]

# ----------------------------
# Model
# ----------------------------
class Item(BaseModel):
    name: str
    description: Optional[str] = Field(default=None, title="Item description", max_length=300)
    price: Optional[float] = None
    tax: Optional[float] = None

# ----------------------------
# 根路由
# ----------------------------
@app.get("/")
def root():
    return {"message": "Hello world"}

@app.get("/ping")
def ping():
    return {"message": "pong"}

# ----------------------------
# 固定路由，放在動態路由前面
# ----------------------------
@app.get("/items/prices")
def get_item_prices():
    return [{"name": item["name"], "total_price": item["price"] + item["tax"]} for item in items_db]

@app.get("/items/max-price")
def get_max_price_item():
    return max(items_db, key=lambda x: x["price"])

@app.get("/items/avg-price")
def get_avg_price():
    avg = sum(item["price"] for item in items_db) / len(items_db)
    return {"average_price": avg}

# ----------------------------
# 動態路由
# ----------------------------
@app.get("/items/id/{item_id}")
def read_item(item_id: int = Path(..., ge=0, le=1000)):
    if item_id >= len(items_db):
        return {"error": "Item not found"}
    return items_db[item_id]

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return items_db[skip: skip + limit]

@app.post("/items/")
def create_item(item: Item):
    item_dict = item.dict()
    if item.price is not None and item.tax is not None:
        item_dict["price_with_tax"] = item.price + item.tax
    items_db.append(item_dict)
    return item_dict
