"""DatabaseManager"""
from contextlib import contextmanager
from threading import Lock

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.util import quote_plus

from app.config import ConfigManager


class Database:
    """DatabaseManager implementing Singleton for the database object."""
    _instance = None
    _lock = Lock()  # To make the singleton thread-safe

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    config = ConfigManager().get_config()
                    cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __get_engine(self) -> Engine:
        config = ConfigManager().get_config()
        database_name = config.PG_DATABASE
        endpoint = config.PG_ENDPOINT
        user = config.PG_USER
        password = config.PG_PASSWORD
        return create_engine(f"postgresql+psycopg2://{user}:%s@{endpoint}/{database_name}" % quote_plus(password))

    @contextmanager
    def connect(self):
        engine = self.__get_engine()
        try:
            with engine.connect() as connection:
                yield connection
        finally:
            if "connection" in locals():
                connection.close()

    @contextmanager
    def get_session(self):
        engine = self.__get_engine()
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        try:
            yield session
        finally:
            if "session" in locals():
                session.close()
