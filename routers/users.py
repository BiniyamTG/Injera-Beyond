from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from bson import ObjectId
from models import User
from database import user_collection
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(prefix="/users", tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "favorites": [str(f) for f in user.get("favorites", [])],
        "tried_items": [str(t) for t in user.get("tried_items", [])],
        "created_at": str(user.get("created_at")),
    }

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        user = await user_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return user_serializer(user)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/")
async def create_user(user: User):
    if await user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = user.dict()
    new_user["password"] = pwd_context.hash(new_user["password"])
    result = await user_collection.insert_one(new_user)
    created_user = await user_collection.find_one({"_id": result.inserted_id})
    return user_serializer(created_user)

@router.get("/")
async def get_users(user: dict = Depends(get_current_user)):
    users = []
    async for u in user_collection.find():
        users.append(user_serializer(u))
    return users

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_collection.find_one({"email": form_data.username})
    if not user or not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"sub": str(user["_id"]), "exp": datetime.utcnow() + timedelta(hours=1)}, SECRET_KEY, ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}