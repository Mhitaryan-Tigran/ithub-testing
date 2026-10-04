from pydantic import BaseModel, ConfigDict, Field

from utils.fakers import random_email, random_number, random_string, random_username


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(default_factory=lambda: random_number(10**6, 10**7))
    username: str = Field(default_factory=random_username, min_length=3)
    first_name: str = Field(alias="firstName", default_factory=random_string)
    last_name: str = Field(alias="lastName", default_factory=random_string)
    email: str = Field(default_factory=random_email, pattern=r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$")
    password: str = Field(default_factory=random_string, min_length=8)
    phone: str = Field(default_factory=lambda: "+7" + str(random_number(10**9, 10**10 - 1)))
    user_status: int = Field(alias="userStatus", default=1, ge=0)


class ApiResponse(BaseModel):
    code: int
    type: str
    message: str
