from typing import Optional

from sqlalchemy.orm import Session

from app.models import RestaurantModel
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate
from app.repositories.base import BaseRepository


class RestaurantRepository(BaseRepository[RestaurantModel, RestaurantCreate, RestaurantUpdate]):
    model = RestaurantModel

    def get_by_name(self, session: Session, *, name: str) -> Optional[RestaurantModel]:  # noqa: E501

        return session.query(self.model).filter(
            self.model.name == name
        ).first()

    def get_by_uuid(self, session: Session, *, uuid: str) -> Optional[RestaurantModel]:  # noqa: E501
        return session.query(self.model).filter(
            self.model.uuid == uuid
        ).first()
