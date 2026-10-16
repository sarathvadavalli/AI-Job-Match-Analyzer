from pymongo import ASCENDING, MongoClient

from myapp.core.config import get_settings


settings = get_settings()

client = MongoClient(
    settings.mongodb_uri,
    connect=False,
    maxPoolSize=5,
    minPoolSize=0,
    maxIdleTimeMS=60_000,
    serverSelectionTimeoutMS=settings.mongodb_timeout_ms,
    connectTimeoutMS=settings.mongodb_timeout_ms,
    socketTimeoutMS=10_000,
)
database = client[settings.mongodb_database]
users_collection = database["users"]
profiles_collection = database["profiles"]


def init_db() -> None:
    users_collection.create_index(
        [("email", ASCENDING)],
        unique=True,
        name="unique_user_email",
    )

    users_collection.create_index(
        [("username", ASCENDING)],
        unique=True,
        name="unique_username",
    )

    profiles_collection.create_index(
        [("user_id", ASCENDING)],
        unique=True,
        name="unique_profile_user_id",
    )


def close_db() -> None:
    client.close()
