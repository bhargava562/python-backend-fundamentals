from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routes import book_routes, user_routes
from app.errors import validation_exception_handler, http_exception_handler

app = FastAPI(title="CRUD Assignment API")

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

app.include_router(book_routes.router)
app.include_router(user_routes.router)

@app.get("/")
def home():
    return {"message": "FastAPI CRUD Assignment"}
