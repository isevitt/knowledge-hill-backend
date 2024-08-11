from typing import Optional
from mock_db import mock_items
from fastapi import FastAPI
import random
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def get_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/items/next_item")
def get_next_item():
    # currently gets a random entruy from the mock_items list
    random_item: dict = get_random_item()
    return random_item


def get_random_item() -> dict:
    random_item = mock_items[random.randint(0, len(mock_items) - 1)]
    return random_item