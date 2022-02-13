from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, root_validator
from pydantic.utils import GetterDict


class RestaurantIn(BaseModel):
    name: str = Field(title="Restaurant Name", min_length=1)
    address: str = Field(title="Restaurant Address", min_length=1)


class RestaurantCreate(BaseModel):
    name: str = Field(title="Restaurant Name", min_length=1)
    address: str = Field(title="Restaurant Address", min_length=1)


class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(title="Restaurant Name", min_length=1)
    address: Optional[str] = Field(title="Restaurant Address", min_length=1)


class RestaurantOut(BaseModel):
    id: str = Field(title="Restaurant ID")  # noqa
    name: Optional[str] = Field(title="Restaurant Name", min_length=1)
    address: Optional[str] = Field(title="Restaurant Address", min_length=1)

    class Config:
        orm_mode = True

    @root_validator(pre=True)
    def set_recognizable_id(cls, obj: GetterDict) -> Dict[str, Any]:
        restaurant_dict = dict(obj.items())
        restaurant_dict['id'] = obj._obj.uuid
        return restaurant_dict
