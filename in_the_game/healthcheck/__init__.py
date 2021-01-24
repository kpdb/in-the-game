from fastapi import APIRouter

from .models import HealthCheck

router = APIRouter()


@router.get("/", response_model=HealthCheck)
async def health_check():
    return HealthCheck(status="healthy")
