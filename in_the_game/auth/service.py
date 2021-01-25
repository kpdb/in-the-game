from typing import Optional

from . import handlers, repository
from .models import TokenResponse, UserLogin


async def login_user(user_login: UserLogin) -> Optional[TokenResponse]:
    user_data = await repository.get_user_by_email(user_login.email)
    if user_data and user_login.password == user_data['password']:
        token = handlers.sign_with_token(user_data['email'])
        return TokenResponse(access_token=token)
    return None
