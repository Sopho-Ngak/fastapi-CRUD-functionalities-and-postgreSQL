from fastapi import FastAPI
from routers import posts

app = FastAPI(title="CRUD app with FastAPI and PostgreSQL", version="1.0.0")

app.include_router(posts.router, prefix="/api/v1", tags=["posts"])

@app.get("/")
def read_root():
    return {"message": "Welcome to CRUD app with FastAPI and PostgreSQL"}