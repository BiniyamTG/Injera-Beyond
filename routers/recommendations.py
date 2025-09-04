from fastapi import APIRouter, HTTPException
from typing import Optional
from bson import ObjectId
from database import food_collection, drink_collection
from routers.foods import food_serializer
from routers.drinks import drink_serializer
from random import choice
from geopy.distance import geodesic

router = APIRouter(prefix="/recommendation", tags=["recommendations"])

@router.get("/random")
async def get_random_item(lang: str = "en"):
    collection = choice([food_collection, drink_collection])
    pipeline = [{"$sample": {"size": 1}}]
    async for item in collection.aggregate(pipeline):
        serialized = food_serializer(item) if collection == food_collection else drink_serializer(item)
        if lang == "am" and item.get("name_amharic"):
            serialized["name"] = item["name_amharic"]
        return serialized
    raise HTTPException(status_code=404, detail="No items found")

@router.get("/by-region/{region}")
async def get_by_region(region: str, lang: str = "en"):
    items = []
    async for food in food_collection.find({"region": region}):
        serialized = food_serializer(food)
        if lang == "am" and food.get("name_amharic"):
            serialized["name"] = food["name_amharic"]
        items.append(serialized)
    async for drink in drink_collection.find({"region": region}):
        serialized = drink_serializer(drink)
        if lang == "am" and drink.get("name_amharic"):
            serialized["name"] = drink["name_amharic"]
        items.append(serialized)
    if not items:
        raise HTTPException(status_code=404, detail="No items found in this region")
    return items

@router.get("/daily")
async def get_daily_suggestion(lang: str = "en"):
    pipeline = [{"$sample": {"size": 1}}]
    async for item in food_collection.aggregate(pipeline):
        serialized = food_serializer(item)
        if lang == "am" and item.get("name_amharic"):
            serialized["name"] = item["name_amharic"]
        return serialized
    async for item in drink_collection.aggregate(pipeline):
        serialized = drink_serializer(item)
        if lang == "am" and item.get("name_amharic"):
            serialized["name"] = item["name_amharic"]
        return serialized
    raise HTTPException(status_code=404, detail="No items found")

@router.get("/nearby")
async def get_nearby_items(lat: float, lon: float, lang: str = "en"):
    items = []
    user_location = (lat, lon)
    async for food in food_collection.find():
        for restaurant in food.get("restaurant_suggestions", []):
            parts = restaurant.split(", ")
            if len(parts) >= 4:
                try:
                    restaurant_location = (float(parts[2]), float(parts[3]))
                    if geodesic(user_location, restaurant_location).km < 10:
                        serialized = food_serializer(food)
                        if lang == "am" and food.get("name_amharic"):
                            serialized["name"] = food["name_amharic"]
                        items.append(serialized)
                except ValueError:
                    continue
    if not items:
        raise HTTPException(status_code=404, detail="No items found nearby")
    return items