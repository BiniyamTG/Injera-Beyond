from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from database import user_collection, food_collection, drink_collection
from routers.users import get_current_user
from routers.foods import food_serializer
from routers.drinks import drink_serializer

router = APIRouter(tags=["favorites"])

@router.post("/favorites/{item_id}")
async def add_favorite(item_id: str, user: dict = Depends(get_current_user)):
    item_oid = ObjectId(item_id)
    if not await food_collection.find_one({"_id": item_oid}) and not await drink_collection.find_one({"_id": item_oid}):
        raise HTTPException(status_code=404, detail="Item not found")
    result = await user_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$addToSet": {"favorites": item_oid}}
    )
    if result.modified_count:
        return {"message": "Added to favorites"}
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/tried/{item_id}")
async def add_tried(item_id: str, user: dict = Depends(get_current_user)):
    item_oid = ObjectId(item_id)
    if not await food_collection.find_one({"_id": item_oid}) and not await drink_collection.find_one({"_id": item_oid}):
        raise HTTPException(status_code=404, detail="Item not found")
    result = await user_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$addToSet": {"tried_items": item_oid}}
    )
    if result.modified_count:
        return {"message": "Marked as tried"}
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/favorites")
async def get_favorites(user: dict = Depends(get_current_user)):
    user = await user_collection.find_one({"_id": ObjectId(user["id"])})
    favorites = []
    for item_id in user.get("favorites", []):
        food = await food_collection.find_one({"_id": ObjectId(item_id)})
        if food:
            favorites.append(food_serializer(food))
        else:
            drink = await drink_collection.find_one({"_id": ObjectId(item_id)})
            if drink:
                favorites.append(drink_serializer(drink))
    return favorites

@router.get("/tried")
async def get_tried(user: dict = Depends(get_current_user)):
    user = await user_collection.find_one({"_id": ObjectId(user["id"])})
    tried_items = []
    for item_id in user.get("tried_items", []):
        food = await food_collection.find_one({"_id": ObjectId(item_id)})
        if food:
            tried_items.append(food_serializer(food))
        else:
            drink = await drink_collection.find_one({"_id": ObjectId(item_id)})
            if drink:
                tried_items.append(drink_serializer(drink))
    return tried_items