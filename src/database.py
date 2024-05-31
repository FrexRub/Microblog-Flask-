from src.config import setting

db_url = (
    f"postgresql+psycopg2://{setting.postgres_user}:{setting.postgres_password}@{setting.postgres_host}:"
    f"{setting.postgres_port}/{setting.postgres_db}"
)

# для локальной работы
# DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/mblog_db"




