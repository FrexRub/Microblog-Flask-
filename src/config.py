import os
from pathlib import Path
from dataclasses import dataclass

BASE_DIR = Path(__file__).parent

@dataclass(slots=True)
class Setting:
    # postgres_user: str = os.getenv("POSTGRES_USER", "test")
    # postgres_password: str = os.getenv("POSTGRES_PASSWORD", "test")
    # postgres_db: str = os.getenv("POSTGRES_DB", "testdb")
    # postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    # postgres_port: int = os.getenv("POSTGRES_PORT", 5438)

    postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "admin")
    postgres_db: str = os.getenv("POSTGRES_DB", "mblog_db")
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = os.getenv("POSTGRES_PORT", 5432)


setting = Setting()
