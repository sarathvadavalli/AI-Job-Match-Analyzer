from pymongo import ASCENDING, MongoClient

from myapp.core.config import get_settings


settings = get_settings()
client = MongoClient(settings.mongodb_uri)
database = client[settings.mongodb_database]
users_collection = database["users"]


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


def close_db() -> None:
    client.close()
