from fastapi import APIRouter
from core.api.router.v1 import router as router_v1


router = APIRouter()


router.include_router(router_v1, prefix="/api/v1")