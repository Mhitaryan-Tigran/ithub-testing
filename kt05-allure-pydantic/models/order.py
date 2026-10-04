from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel

from utils.fakers import random_number


class Order(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(default_factory=lambda: random_number(1, 10))
    pet_id: int = Field(alias="petId", default_factory=random_number)
    quantity: int = Field(default_factory=lambda: random_number(1, 5), ge=1)
    ship_date: str = Field(alias="shipDate", default="2026-10-04T12:00:00.000+0000")
    status: Literal["placed", "approved", "delivered"] = "placed"
    complete: bool = False


class Inventory(RootModel):
    root: dict[str, int]
