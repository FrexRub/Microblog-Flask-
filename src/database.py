from flask_sqlalchemy import SQLAlchemy
import psycopg2

from src.config import setting

db = SQLAlchemy()

db_url = (
    f"postgresql+psycopg2://{setting.postgres_user}:{setting.postgres_password}@{setting.postgres_host}:"
    f"{setting.postgres_port}/{setting.postgres_db}"
)

# для локальной работы
# DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/mblog_db"




