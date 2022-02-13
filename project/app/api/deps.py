# Standard Library
from typing import Any, Type, TypeVar, Iterator
from app.db.base import BaseModel as DBBaseModel
from app.db.session import SessionMaker
from app.repositories import PersonRepository, PizzaRepository, RestaurantRepository

ModelType = TypeVar('ModelType', bound=DBBaseModel)


def get_session() -> Iterator[Any]:
    session = SessionMaker()
    try:
        yield session
    finally:
        session.close()


def get_person_repo() -> PersonRepository:
    return PersonRepository()


def get_restaurant_repo() -> RestaurantRepository:
    return RestaurantRepository()


def get_pizza_repo() -> PizzaRepository:
    return PizzaRepository()
