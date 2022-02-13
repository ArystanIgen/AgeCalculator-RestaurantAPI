from typing import Iterator

from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.main import main_app
from app.db.base import BaseModel
from app.api.deps import get_session
from app.tests.unit.fixtures import *  # noqa
from app.tests.functional.api.fixtures import *  # noqa


@fixture(scope="function")
def session() -> Iterator[Session]:
    db_engine = create_engine('sqlite:///./test.db', connect_args={'check_same_thread': False})
    connection = db_engine.connect()
    BaseModel.metadata.create_all(bind=db_engine)
    session = Session(bind=db_engine)
    yield session
    session.close()
    BaseModel.metadata.drop_all(bind=db_engine)
    connection.close()   # pragma: no cover


@fixture(scope="function")
def client(session: Iterator[Session]) -> TestClient:
    def _get_db_override() -> Iterator[Session]:
        return session                                  # pragma: no cover

    main_app.dependency_overrides[get_session] = _get_db_override
    return TestClient(main_app)
