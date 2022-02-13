# Standard Library
import logging
from typing import Any, List, Type, Generic, TypeVar, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder


from app.db.base import BaseModel as DBBaseModel

logger = logging.getLogger(__name__)


ModelType = TypeVar('ModelType', bound=DBBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).
    * `model`: A SQLAlchemy model class
    """
    model: Type[ModelType]

    def get(self, session: Session, *, id_: Any, with_for_update: bool = False)-> Optional[ModelType]: # noqa
        query = session.query(self.model)
        if with_for_update:
            query = query.with_for_update()
        return query.filter(self.model.id == id_).first()

    def get_multi(
        self, session: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return session.query(self.model).offset(skip).limit(limit).all()
    def create(self, session: Session, *, obj_in: CreateSchemaType)-> Optional[ModelType]: # noqa
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)  # type: ignore
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj
        except Exception as e:
            logger.error(e)
            session.rollback()
            return None

    def update(self, session: Session, *, instance: ModelType) -> Optional[ModelType]:
        session.commit()
        return instance

    def remove(self, session: Session, *, id_: int) -> Optional[ModelType]:
        if (instance := self.get(session=session, id_=id_)) is not None:
            session.delete(instance)
            session.commit()
            return instance
        else:
            return None
