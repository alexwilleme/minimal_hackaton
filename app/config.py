"""BaseSettings"""
from pathlib import Path
from threading import Lock
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Config"""
    CLOUD_ID: str
    AWS_REGION: str
    AWS_PROFILE_NAME: Optional[str] = None
    S3_BUCKET: str
    # related to Postgres database
    PG_DATABASE: str
    PG_USER: str
    PG_ENDPOINT: str
    PG_PASSWORD: str


class ConfigManager:
    """ConfigManager implementing Singleton for the settings object."""
    _instance = None
    _config: Optional[Config] = None
    _lock = Lock()  # To make the singleton thread-safe

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    root_path = find_project_root(start_path=Path(__file__))
                    load_dotenv(dotenv_path=f"{root_path}/.env")
                    cls._instance = super(ConfigManager, cls).__new__(cls)
                    cls._instance._config = Config()
        return cls._instance

    def get_config(self) -> Config:
        if self._config is None:
            raise RuntimeError(f"{self.__class__.__name__}.get_config: Config object is None.")
        return self._config


def find_project_root(start_path: Path) -> Path:
    for path in start_path.resolve().parents:
        if (path / "pyproject.toml").exists():
            return path
    raise FileNotFoundError("Project root not found. Please make sure 'pyproject.toml' exists.")
