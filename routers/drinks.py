from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from bson import ObjectId
from models import Drink, Rating
from database import drink_collection
from routers.users import get_current_user

router = APIRouter(prefix="/drinks", tags=["drinks"])

def drink_serializer(drink) -> dict:
    return {
        "id": str(drink["_id"]),
        "name": drink["name"],
        "type": drink.get("type", "drink"),
        "region": drink.get("region"),
        "description": drink.get("description"),
        "photo_urls": drink.get("photo_urls", []),
        "trivia": drink.get("trivia"),
        "name_amharic": drink.get("name_amharic"),
        "ratings": drink.get("ratings", []),
        "created_at": str(drink.get("created_at")),
    }

@router.post("/")
async def create_drink(drink: Drink, user: dict = Depends(get_current_user)):
    new_drink = drink.dict()
    result = await drink_collection.insert_one(new_drink)
    created_drink = await drink_collection.find_one({"_id": result.inserted_id})
    return drink_serializer(created_drink)

@router.get("/")
async def get_drinks(lang: str = "en"):
    drinks = []
    async for drink in drink_collection.find():
        serialized = drink_serializer(drink)
        if lang == "am" and drink.get("name_amharic"):
            serialized["name"] = drink["name_amharic"]
        drinks.append(serialized)
    return drinks

@router.get("/{drink_id}")
async def get_drink(drink_id: str, lang: str = "en"):
    drink = await drink_collection.find_one({"_id": ObjectId(drink_id)})
    if drink:
        serialized = drink_serializer(drink)
        if lang == "am" and drink.get("name_amharic"):
            serialized["name"] = drink["name_amharic"]
        return serialized
    raise HTTPException(status_code=404, detail="Drink not found")

@router.put("/{drink_id}")
async def update_drink(drink_id: str, drink: Drink, user: dict = Depends(get_current_user)):
    update_data = {k: v for k, v in drink.dict().items() if v is not None}
    result = await drink_collection.update_one({"_id": ObjectId(drink_id)}, {"$set": update_data})
    if result.modified_count:
        updated_drink = await drink_collection.find_one({"_id": ObjectId(drink_id)})
        return drink_serializer(updated_drink)
    raise HTTPException(status_code=404, detail="Drink not found")

@router.delete("/{drink_id}")
async def delete_drink(drink_id: str, user: dict = Depends(get_current_user)):
    result = await drink_collection.delete_one({"_id": ObjectId(drink_id)})
    if result.deleted_count:
        return {"message": "Drink deleted"}
    raise HTTPException(status_code=404, detail="Drink not found")

@router.get("/random")
async def get_random_drink(lang: str = "en"):
    pipeline = [{"$sample": {"size": 1}}]
    async for drink in drink_collection.aggregate(pipeline):
        serialized = drink_serializer(drink)
        if lang == "am" and drink.get("name_amharic"):
            serialized["name"] = drink["name_amharic"]
        return serialized
    raise HTTPException(status_code=404, detail="No drinks found")

@router.post("/{drink_id}/rate")
async def rate_drink(drink_id: str, rating: Rating, user: dict = Depends(get_current_user)):
    if not 1 <= rating.score <= 5:
        raise HTTPException(status_code=400, detail="Score must be 1-5")
    result = await drink_collection.update_one(
        {"_id": ObjectId(drink_id)},
        {"$push": {"ratings": {"user_id": user["id"], "score": rating.score}}}
    )
    if result.modified_count:
        return {"message": "Rating added"}
    raise HTTPException(status_code=404, detail="Drink not found")

@router.get("/{drink_id}/share")
async def share_drink(drink_id: str, lang: str = "en"):
    drink = await drink_collection.find_one({"_id": ObjectId(drink_id)})
    if drink:
        name = drink["name_amharic"] if lang == "am" and drink.get("name_amharic") else drink["name"]
        return {"share_text": f"Try {name} in Ethiopia! {drink['description']}"}
    raise HTTPException(status_code=404, detail="Drink not found")

@router.get("/popular")
async def get_popular_drinks(limit: int = 10, lang: str = "en"):
    pipeline = [
        {"$lookup": {
            "from": "users",
            "localField": "_id",
            "foreignField": "tried_items",
            "as": "tried_by"
        }},
        {"$addFields": {"tried_count": {"$size": "$tried_by"}}},
        {"$sort": {"tried_count": -1}},
        {"$limit": limit}
    ]
    drinks = []
    async for drink in drink_collection.aggregate(pipeline):
        serialized = drink_serializer(drink)
        if lang == "am" and drink.get("name_amharic"):
            serialized["name"] = drink["name_amharic"]
        drinks.append(serialized)
    return drinks