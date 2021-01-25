from fastapi import APIRouter

router = APIRouter()


@router.post("/auth")
async def authorize_user():
    pass


@router.get("/subscription")
async def get_user_subscription(user_id: int):
    pass


@router.put("/subscription")
async def update_user_subscription(user_id: int, subscription):
    pass
