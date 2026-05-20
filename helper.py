from datetime import datetime, timedelta
import jwt
from setting import settings

def create_access_token(user_id: int):
    exp_time = datetime.utcnow() + timedelta(minutes=15)

    payload = {
        "id": user_id,
        "exp": exp_time.timestamp(),
        "token_type": "access"
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def create_refresh_token(user_id: int):
    exp_time = datetime.utcnow() + timedelta(days=7)

    payload = {
        "id": user_id,
        "exp": exp_time.timestamp(),
        "token_type": "refresh"
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )