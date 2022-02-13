from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import PizzaModel
from app.schemas.pizza import PizzaCreate, PizzaUpdate
from app.repositories.base import BaseRepository


class PizzaRepository(BaseRepository[PizzaModel, PizzaCreate, PizzaUpdate]):
    model = PizzaModel

    def get_by_name(self, session: Session, *, name: str) -> Optional[PizzaModel]:  # noqa: E501

        return session.query(self.model).filter(
            self.model.name == name
        ).first()

    def get_by_uuid(self, session: Session, *, uuid: str,restaurant_id:int) -> Optional[PizzaModel]:  # noqa: E501
        return session.query(self.model).filter(
            self.model.uuid == uuid,
            self.model.restaurant_id == restaurant_id
        ).first()

    def get_list_of_pizzas(
            self,
            session: Session,
            *, restaurant_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[PizzaModel]:
        return session.query(self.model).filter(
            self.model.restaurant_id == restaurant_id
        ).offset(skip).limit(limit).all()
