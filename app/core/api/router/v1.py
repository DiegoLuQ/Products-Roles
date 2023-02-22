from .router_product import router as route_product
from .router_login import router as route_login
from fastapi import APIRouter

router = APIRouter()


router.include_router(route_product, prefix="/products", tags=["Products"])
router.include_router(route_login, prefix="/login", tags=["Login"], include_in_schema=False)