import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    mongodb_database: str = os.getenv("MONGODB_DATABASE", "jd_extractor")
    mongodb_timeout_ms: int = int(os.getenv("MONGODB_TIMEOUT_MS", "5000"))
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-this-secret")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_access_token_expire_minutes: int = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
