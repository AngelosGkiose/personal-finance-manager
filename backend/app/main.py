from fastapi import FastAPI

from app.routers.auth_router import router as auth_router
from app.routers.category_router import router as category_router
from app.routers.expense_router import router as expense_router
from app.routers.income_router import router as income_router
from app.routers.dashboard_router import router as dashboard_router
from app.routers.obligation_router import router as obligation_router


app = FastAPI(
    title="Personal Finance Manager API",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(category_router)
app.include_router(expense_router)
app.include_router(income_router)
app.include_router(dashboard_router)
app.include_router(obligation_router)



@app.get("/")
def root():
    return {"message": "Personal Finance Manager API is running"}