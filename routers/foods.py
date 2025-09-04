from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from bson import ObjectId
from models import Food, Rating
from database import food_collection
from routers.users import get_current_user

router = APIRouter(prefix="/foods", tags=["foods"])

def food_serializer(food) -> dict:
    return {
        "id": str(food["_id"]),
        "name": food["name"],
        "type": food.get("type", "food"),
        "region": food.get("region"),
        "difficulty": food.get("difficulty"),
        "spicy_level": food.get("spicy_level"),
        "description": food.get("description"),
        "ingredients": food.get("ingredients", []),
        "photo_urls": food.get("photo_urls", []),
        "restaurant_suggestions": food.get("restaurant_suggestions", []),
        "trivia": food.get("trivia"),
        "vegetarian": food.get("vegetarian", False),
        "name_amharic": food.get("name_amharic"),
        "ratings": food.get("ratings", []),
        "created_at": str(food.get("created_at")),
    }

@router.post("/")
async def create_food(food: Food, user: dict = Depends(get_current_user)):
    new_food = food.dict()
    result = await food_collection.insert_one(new_food)
    created_food = await food_collection.find_one({"_id": result.inserted_id})
    return food_serializer(created_food)

@router.get("/")
async def get_foods(vegetarian: Optional[bool] = None, spicy_level: Optional[str] = None, lang: str = "en"):
    query = {}
    if vegetarian is not None:
        query["vegetarian"] = vegetarian
    if spicy_level:
        query["spicy_level"] = spicy_level
    foods = []
    async for food in food_collection.find(query):
        serialized = food_serializer(food)
        if lang == "am" and food.get("name_amharic"):
            serialized["name"] = food["name_amharic"]
        foods.append(serialized)
    return foods

@router.get("/{food_id}")
async def get_food(food_id: str, lang: str = "en"):
    food = await food_collection.find_one({"_id": ObjectId(food_id)})
    if food:
        serialized = food_serializer(food)
        if lang == "am" and food.get("name_amharic"):
            serialized["name"] = food["name_amharic"]
        return serialized
    raise HTTPException(status_code=404, detail="Food not found")

@router.put("/{food_id}")
async def update_food(food_id: str, food: Food, user: dict = Depends(get_current_user)):
    update_data = {k: v for k, v in food.dict().items() if v is not None}
    result = await food_collection.update_one({"_id": ObjectId(food_id)}, {"$set": update_data})
    if result.modified_count:
        updated_food = await food_collection.find_one({"_id": ObjectId(food_id)})
        return food_serializer(updated_food)
    raise HTTPException(status_code=404, detail="Food not found")

@router.delete("/{food_id}")
async def delete_food(food_id: str, user: dict = Depends(get_current_user)):
    result = await food_collection.delete_one({"_id": ObjectId(food_id)})
    if result.deleted_count:
        return {"message": "Food deleted"}
    raise HTTPException(status_code=404, detail="Food not found")

@router.get("/random")
async def get_random_food(lang: str = "en"):
    pipeline = [{"$sample": {"size": 1}}]
    async for food in food_collection.aggregate(pipeline):
        serialized = food_serializer(food)
        if lang == "am" and food.get("name_amharic"):
            serialized["name"] = food["name_amharic"]
        return serialized
    raise HTTPException(status_code=404, detail="No foods found")

@router.get("/quiz")
async def get_quiz():
    pipeline = [{"$sample": {"size": 4}}]
    foods = []
    async for food in food_collection.aggregate(pipeline):
        foods.append(food)
    if not foods:
        raise HTTPException(status_code=404, detail="No foods found")
    correct_food = foods[0]
    return {
        "ingredients": correct_food.get("ingredients", []),
        "options": [f["name"] for f in foods],
        "correct_answer": correct_food["name"]
    }

@router.post("/{food_id}/rate")
async def rate_food(food_id: str, rating: Rating, user: dict = Depends(get_current_user)):
    if not 1 <= rating.score <= 5:
        raise HTTPException(status_code=400, detail="Score must be 1-5")
    result = await food_collection.update_one(
        {"_id": ObjectId(food_id)},
        {"$push": {"ratings": {"user_id": user["id"], "score": rating.score}}}
    )
    if result.modified_count:
        return {"message": "Rating added"}
    raise HTTPException(status_code=404, detail="Food not found")

@router.get("/{food_id}/share")
async def share_food(food_id: str, lang: str = "en"):
    food = await food_collection.find_one({"_id": ObjectId(food_id)})
    if food:
        name = food["name_amharic"] if lang == "am" and food.get("name_amharic") else food["name"]
        return {"share_text": f"Try {name} in Ethiopia! {food['description']}"}
    raise HTTPException(status_code=404, detail="Food not found")

@router.get("/popular")
async def get_popular_foods(limit: int = 10, lang: str = "en"):
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
    foods = []
    async for food in food_collection.aggregate(pipeline):
        serialized = food_serializer(food)
        if lang == "am" and food.get("name_amharic"):
            serialized["name"] = food["name_amharic"]
        foods.append(serialized)
    return foods