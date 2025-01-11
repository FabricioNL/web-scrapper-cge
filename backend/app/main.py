from fastapi import FastAPI
from app.routers import floods

app = FastAPI()

app.include_router(floods.router, prefix="/api", tags=["floods"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Flood Data API"}
