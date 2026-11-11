from fastapi import APIRouter
from app.api.v1.endpoints_cbt import router as cbt_router
from app.api.v1.endpoints_mood import router as mood_router

api_v1_router = APIRouter()

api_v1_router.include_router(cbt_router)
api_v1_router.include_router(mood_router)
