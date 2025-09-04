from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import foods, drinks, users, recommendations, favorites

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(foods.router)
app.include_router(drinks.router)
app.include_router(users.router)
app.include_router(recommendations.router)
app.include_router(favorites.router)

@app.get("/")
async def root():
    return {"message": "API running"}