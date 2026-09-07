from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

# USERNAME_PATTERN = r"^(?!.*[_-]{2})[A-Za-z0-9](?:[A-Za-z0-9_-]*[A-Za-z0-9])?$"
# EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

class UserCreate(BaseModel):
    name: str
    username: str = Field(..., min_length=3, max_length=16)
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not value.isascii():
            raise ValueError("Username must contain only ASCII characters.")

        if not value[0].isalnum() or not value[-1].isalnum():
            raise ValueError(
                "Username must start and end with a letter or digit."
            )

        if not all(c.isalnum() or c in "_-" for c in value):
            raise ValueError(
                "Username can contain only letters, digits, '_' and '-'."
            )

        if "__" in value or "--" in value or "_-" in value or "-_" in value:
            raise ValueError(
                "Username cannot contain consecutive '_' or '-'."
            )

        return value

    # @field_validator("email")
    # @classmethod
    # def validate_email(cls, email: str) -> str:
    #     email = email.strip().lower()

    #     if email.count("@") != 1:
    #         raise ValueError("Invalid email format.")

    #     first_part, domain_part = email.split("@", 1)

    #     if not first_part or not domain_part:
    #         raise ValueError("Invalid email format.")

    #     # first_part validation
    #     if not first_part[0].isalnum() or not first_part[-1].isalnum():
    #         raise ValueError("Invalid email format.")

    #     if ".." in first_part:
    #         raise ValueError("Invalid email format.")

    #     if not all(c.isalnum() or c in "._+-" for c in first_part):
    #         raise ValueError("Invalid email format.")

    #     # domain_part validation
    #     if ".." in domain_part:
    #         raise ValueError("Invalid email format.")

    #     if not domain_part[0].isalnum() or not domain_part[-1].isalnum():
    #         raise ValueError("Invalid email format.")

    #     domain_parts = domain_part.split(".")

    #     if len(domain_parts) < 2:
    #         raise ValueError("Invalid email format.")

    #     for part in domain_parts:
    #         if not part:
    #             raise ValueError("Invalid email format.")

    #         if not part[0].isalnum() or not part[-1].isalnum():
    #             raise ValueError("Invalid email format.")

    #         if not all(c.isalnum() or c == "-" for c in part):
    #             raise ValueError("Invalid email format.")

    #     return email


class UserLogin(BaseModel):
    identifier: str = Field(..., min_length=1)
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    message: str


class UserProfile(BaseModel):
    name: str
    email: str
    created_at: datetime
    last_login_at: datetime | None = None
