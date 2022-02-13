from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, root_validator
from pydantic.utils import GetterDict


class PizzaIn(BaseModel):
    name: str = Field(title="Pizza Name", min_length=1)
    cheese_type: str = Field(title="Cheese Type", min_length=1)
    dough_thickness: str = Field(title="Dough Thickness", min_length=1)
    secret_ingredient: str = Field(title="Secret Ingredient", min_length=1)


class PizzaCreate(BaseModel):
    restaurant_id: int
    name: str = Field(title="Pizza Name", min_length=1)
    cheese_type: str = Field(title="Cheese Type", min_length=1)
    dough_thickness: str = Field(title="Dough Thickness", min_length=1)
    secret_ingredient: str = Field(title="Secret Ingredient", min_length=1)


class PizzaUpdate(BaseModel):
    name: Optional[str] = Field(title="Pizza Name", min_length=1)
    cheese_type: Optional[str] = Field(title="Cheese Type", min_length=1)
    dough_thickness: Optional[str] = Field(title="Dough Thickness", min_length=1)
    secret_ingredient: Optional[str] = Field(title="Secret Ingredient", min_length=1)


class PizzaOut(BaseModel):
    id: str = Field(title="Pizza ID")  # noqa
    name: str = Field(title="Pizza Name", min_length=1)
    cheese_type: str = Field(title="Cheese Type", min_length=1)
    dough_thickness: str = Field(title="Dough Thickness", min_length=1)
    secret_ingredient: str = Field(title="Secret Ingredient", min_length=1)

    class Config:
        orm_mode = True

    @root_validator(pre=True)
    def set_recognizable_id(cls, obj: GetterDict) -> Dict[str, Any]:
        pizza_dict = dict(obj.items())
        pizza_dict['id'] = obj._obj.uuid
        return pizza_dict
