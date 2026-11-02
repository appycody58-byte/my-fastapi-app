from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory database representation
db = []

# Pydantic model for data validation
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.get('/')
def read_root():
    return {'message': 'Welcome to your first FastAPI app with multiple endpoints!'}

# Create a new item (POST)
@app.post('/items/', response_model=Item)
def create_item(item: Item):
    db.append(item.model_dump())
    return item

# Get all items (GET)
@app.get('/items/', response_model=List[dict])
def read_items():
    return db

# Get single item by ID
@app.get('/items/{item_id}')
def read_item(item_id: int):
    if item_id < 0 or item_id >= len(db):
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]
