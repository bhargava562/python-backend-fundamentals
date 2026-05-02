from fastapi import FastAPI
from app.api import auth_routes, user_routes

app = FastAPI(title="JWT Auth & RBAC API")

app.include_router(auth_routes.router)
app.include_router(user_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to Day 7: Authentication & Authorization"}