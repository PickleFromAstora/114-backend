from typing import Annotated
from Fastapi import FastAPI,BodyPath
from pydantic import BaseModel,field
class Item(BaseModel):
    name:str
    description: str | None =field(
default=None,title="Ted description of the item",max_length=300
    )
    price: float | None=None



    app= FastAPI()
    @app.get("/")
    async def root():
        return{"message":"Hello world"}
    @app.get("/item/{item_id}")
    async def read_items(item_id):
        return{"item_id" : item_id}
    @app.get("/item/{item_id}")
    async def read_item(skip : int = 0 , limit: int =10):
        return fake_items_db[skip : skip + limit]
    fake_item_db = [
        {"item-name":"foo"},
        {"item-name":"bar"},
        {"item-name":"baz"},
    ]
    @app.post("/items/")
    async def create_item(item: Item):
        item.dict = item.model_dump() # item.dict()
        if item.tax is not None:
            price_with_tax = item.price + item.tax
            item_dict.update({"price_with_tax":price_with_tax})
        return item_dict
    


    ...

    @app.put("/items/{item_id}")
    async def update_item(
        item_id:Annotated[int,Path(title="The ID of the item rto get",ge=0,le=1000)],
        q:str | None =None,
        item: Item | None =None,
    ):
        result = {"item_id" : item_id}
        if q:
            result.update({"q":q})
        if item:
            result.update({"item":item})
        return result
    ...
    @app.put("/items/{item_id}")
    async def update_item(item_id: int, item:Annotated[Item, Body(embed=Truerue)]):
        results = {"itec_id": item_id, "item": item}
        return results
