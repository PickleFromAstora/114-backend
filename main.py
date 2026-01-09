from typing import Optional, Annotated
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field

app = FastAPI()

# ----------------------------
# 假資料庫
# ----------------------------
fake_items_db = [
    {"item_name": "foo", "price": 10.0, "tax": 1.0},
    {"item_name": "bar", "price": 20.0, "tax": 2.0},
    {"item_name": "baz", "price": 30.0, "tax": 3.0},
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
# 基本測試路由
# ----------------------------
@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/ping")
async def ping():
    return {"message": "pong"}

# ----------------------------
# 靜態路由
# ----------------------------
@app.get("/items/names")
async def get_item_names():
    return [item["item_name"] for item in fake_items_db]

@app.get("/items/prices")
async def get_item_prices():
    return [
        {"item_name": item["item_name"], "total_price": item["price"] + item["tax"]}
        for item in fake_items_db
    ]

@app.get("/items/max-price")
async def get_max_price():
    max_item = max(fake_items_db, key=lambda x: x["price"])
    return max_item

@app.get("/items/min-price")
async def get_min_price():
    min_item = min(fake_items_db, key=lambda x: x["price"])
    return min_item

@app.get("/items/avg-price")
async def get_avg_price():
    avg = sum(item["price"] for item in fake_items_db) / len(fake_items_db)
    return {"average_price": avg}

# ----------------------------
# 動態路由
# ----------------------------
@app.get("/items/id/{item_id}")
async def read_item(item_id: Annotated[int, Path(ge=0, le=1000)]):
    if item_id < len(fake_items_db):
        return fake_items_db[item_id]
    return {"error": "Item not found"}

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.price is not None and item.tax is not None:
        item_dict["price_with_tax"] = item.price + item.tax
    fake_items_db.append(item_dict)
    return item_dict

@app.put("/items/id/{item_id}")
async def update_item(item_id: Annotated[int, Path(ge=0, le=1000)], item: Item):
    if item_id >= len(fake_items_db):
        return {"error": "Item not found"}
    fake_items_db[item_id].update(item.model_dump())
    return fake_items_db[item_id]
from typing import Optional, Annotated
from fastapi import FastAPI, Path
from pydantic import BaseModel, Field

app = FastAPI()

# ----------------------------
# 假資料庫
# ----------------------------
fake_items_db = [
    {"item_name": "foo", "price": 10.0, "tax": 1.0},
    {"item_name": "bar", "price": 20.0, "tax": 2.0},
    {"item_name": "baz", "price": 30.0, "tax": 3.0},
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
# 基本測試路由
# ----------------------------
@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/ping")
async def ping():
    return {"message": "pong"}

# ----------------------------
# 靜態路由
# ----------------------------
@app.get("/items/names")
async def get_item_names():
    return [item["item_name"] for item in fake_items_db]

@app.get("/items/prices")
async def get_item_prices():
    return [
        {"item_name": item["item_name"], "total_price": item["price"] + item["tax"]}
        for item in fake_items_db
    ]

@app.get("/items/max-price")
async def get_max_price():
    max_item = max(fake_items_db, key=lambda x: x["price"])
    return max_item

@app.get("/items/min-price")
async def get_min_price():
    min_item = min(fake_items_db, key=lambda x: x["price"])
    return min_item

@app.get("/items/avg-price")
async def get_avg_price():
    avg = sum(item["price"] for item in fake_items_db) / len(fake_items_db)
    return {"average_price": avg}

# ----------------------------
# 動態路由
# ----------------------------
@app.get("/items/id/{item_id}")
async def read_item(item_id: Annotated[int, Path(ge=0, le=1000)]):
    if item_id < len(fake_items_db):
        return fake_items_db[item_id]
    return {"error": "Item not found"}

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.price is not None and item.tax is not None:
        item_dict["price_with_tax"] = item.price + item.tax
    fake_items_db.append(item_dict)
    return item_dict

@app.put("/items/id/{item_id}")
async def update_item(item_id: Annotated[int, Path(ge=0, le=1000)], item: Item):
    if item_id >= len(fake_items_db):
        return {"error": "Item not found"}
    fake_items_db[item_id].update(item.model_dump())
    return fake_items_db[item_id]
