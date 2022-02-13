# Standard Library
import datetime

from sqlalchemy import Column, Integer, DateTime  # type: ignore
from sqlalchemy.ext.declarative import as_declarative  # type: ignore


@as_declarative()
class BaseModel(object):
    id = Column(Integer, primary_key=True, autoincrement=True)  # noqa: A003

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )
