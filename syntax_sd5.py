from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

# Create the app
app = FastAPI()

# ----------------------
# Custom Exception Class
# ----------------------
class ResourceNotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message

# ----------------------
# Exception Handler
# ----------------------
@app.exception_handler(ResourceNotFoundError)
async def resource_not_found_handler(request: Request, exc: ResourceNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)}
    )

# ----------------------
# Pydantic Model
# ----------------------
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool

# ----------------------
# Fake In-Memory Storage
# ----------------------
inventory = {
    1: {"name": "Laptop", "description": "15 inch screen", "price": 1200.00, "in_stock": True},
    2: {"name": "Mouse", "description": "Wireless mouse", "price": 25.99, "in_stock": True}
}

# ----------------------
# GET Route with Path Parameter
# ----------------------
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in inventory:
        raise ResourceNotFoundError(f"Item with ID {item_id} not found.")
    return {"item_id": item_id, "data": inventory[item_id]}

# ----------------------
# POST Route with Body Data
# ----------------------
@app.post("/items/")
async def create_item(item: Item):
    new_id = max(inventory.keys()) + 1
    inventory[new_id] = item.dict()
    return {"message": "Item added", "item_id": new_id, "item": item}

# ----------------------
# Query Parameter Example
# ----------------------
@app.get("/search/")
async def search_items(min_price: Optional[float] = 0.0):
    results = []
    for item_id, data in inventory.items():
        if data["price"] >= min_price:
            results.append({"item_id": item_id, "data": data})
    return {"results": results}
