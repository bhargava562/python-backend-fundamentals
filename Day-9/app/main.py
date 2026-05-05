from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database.mongodb import connect_to_mongo, close_mongo_connection
from .api.catalog_routes import router as catalog_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(title="Day 9: MongoDB API", lifespan=lifespan)
app.include_router(catalog_router)