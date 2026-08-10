from fastapi import FastAPI

from app.routers.auth_router import router as auth_router


app = FastAPI(
    title="Personal Finance Manager API",
    version="1.0.0"
)


app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "Personal Finance Manager API is running"}