from uuid import uuid4
from sqlalchemy import Enum, Column, String, Integer, ForeignKey  # type: ignore # noqa
from sqlalchemy.orm import relationship  # type: ignore
from app.db.base import BaseModel


class RestaurantModel(BaseModel):
    __tablename__ = "restaurant"

    uuid = Column(String, unique=True, default=lambda: f"rst_{uuid4()}", comment="Restaurant ID")
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)

    pizza = relationship("PizzaModel", back_populates="restaurant")
