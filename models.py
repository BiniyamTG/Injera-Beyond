from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class Food(BaseModel):
    name: str
    type: str = "food"
    region: str
    difficulty: Optional[str] = None
    spicy_level: Optional[str] = None
    description: Optional[str] = None
    ingredients: List[str] = []
    photo_urls: List[str] = []
    restaurant_suggestions: List[str] = []
    trivia: Optional[str] = None
    vegetarian: Optional[bool] = False
    name_amharic: Optional[str] = None
    ratings: List[dict] = []
    created_at: datetime = datetime.utcnow()

class Drink(BaseModel):
    name: str
    type: str = "drink"
    region: str
    description: Optional[str] = None
    photo_urls: List[str] = []
    trivia: Optional[str] = None
    name_amharic: Optional[str] = None
    ratings: List[dict] = []
    created_at: datetime = datetime.utcnow()

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    favorites: List[str] = []
    tried_items: List[str] = []
    created_at: datetime = datetime.utcnow()

class Rating(BaseModel):
    score: int