from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

from app.core.config import CONFIG

engine = create_engine(CONFIG.db.url, pool_pre_ping=True)
SessionMaker = sessionmaker(autoflush=False, autocommit=False, bind=engine)
