from typing import Optional
from mock_db import mock_items
from fastapi import FastAPI
import random
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://knowledge-hill.onrender.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/next_item")
def get_next_item():
    # currently gets a random entruy from the mock_items list
    random_item: dict = get_random_item()
    return random_item


def get_random_item() -> dict:
    random_item = mock_items[random.randint(0, len(mock_items) - 1)]
    return random_item