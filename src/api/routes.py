from fastapi import APIRouter
from .v1.healthy import router as healthy_router

router = APIRouter(prefix='/v1')

router.include_router(healthy_router, prefix='/route')
