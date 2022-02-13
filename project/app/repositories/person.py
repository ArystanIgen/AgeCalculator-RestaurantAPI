# Standard Library
from typing import Optional

from sqlalchemy.orm import Session

from app.models.person import PersonModel
from app.schemas.person import PersonCreate, PersonUpdate
from app.repositories.base import BaseRepository


class PersonRepository(BaseRepository[PersonModel, PersonCreate, PersonUpdate]):
    model = PersonModel

    def get_by_iin(self, session: Session, *, iin: str) -> Optional[PersonModel]:  # noqa: E501

        return session.query(self.model).filter(
            self.model.iin == iin,
        ).first()

    # def get_list(
    #         self, session: Session, *, iin: str, skip: int = 0,
    #         limit: int = 100,
    # ) -> List[PersonModel]:
    #     return session.query(self.model).filter(
    #         self.model.iin == iin
    #     ).offset(skip).limit(limit).all()
