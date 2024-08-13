from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict

from mock_db import mock_items
from fastapi import FastAPI
import random
import os
import motor.motor_asyncio
from fastapi.middleware.cors import CORSMiddleware
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://knowledge-hill.onrender.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.get_database("knowledge-hill-db")
student_collection = db.get_collection("knowledge-items")

PyObjectId = Annotated[str, BeforeValidator(str)]


class ItemModel(BaseModel):
    """
    Container for a single student record.
    """
    # The primary key for the ItemModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    description: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "description": "How to grow tomatoes",
                "date_created": "2021-01-01 10:10:10.111"
            }
        },
    )

class ItemCollection(BaseModel):
    items: List[ItemModel]


@app.get("/items/", response_description="List items",
         response_model=ItemCollection, response_model_by_alias=False)
async def list_items():
    items = await student_collection.find().to_list(100)
    logging.info(f"items: {items}")
    return ItemCollection(items=items)


@app.get("/items/next", response_description="Get next item",
         response_model=ItemModel, response_model_by_alias=False)
async def get_next_suggested_item():
    pipeline = [{"$sample": {"size": 1}}]
    item = await student_collection.aggregate(pipeline).to_list(1)
    if item:
        return ItemModel(**item)
    raise Exception("No items found")


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