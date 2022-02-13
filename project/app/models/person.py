from sqlalchemy import Enum, Column, String, Integer, ForeignKey  # type: ignore # noqa
from sqlalchemy.orm import relationship  # type: ignore

from app.db.base import BaseModel


class PersonModel(BaseModel):
    __tablename__ = "person"

    iin = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
