from uuid import uuid4
from sqlalchemy import Enum, Column, String, Integer, ForeignKey  # type: ignore # noqa
from sqlalchemy.orm import relationship  # type: ignore
from app.db.base import BaseModel


class PizzaModel(BaseModel):
    __tablename__ = "pizza"

    uuid = Column(String, unique=True, default=lambda: f"pzz_{uuid4()}", comment="Pizza ID")

    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    name = Column(String, unique=True, index=True, nullable=False)
    cheese_type = Column(String, nullable=False)
    dough_thickness = Column(String, nullable=False)
    secret_ingredient = Column(String, nullable=False)

    restaurant = relationship("RestaurantModel", back_populates="pizza")
