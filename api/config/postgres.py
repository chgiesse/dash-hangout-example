from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os

load_dotenv()

# PostgreSQL connection details
ENVIRONMENT = os.environ.get("ENVIRONMENT")

if ENVIRONMENT == 'dev':
    PG_HOST = os.environ.get('PG_DEV_HOST', 'localhost')
    PG_PORT = os.environ.get('PG_DEV_PORT', '5432')
    PG_USER = os.environ.get('PG_DEV_USER', 'postgres')
    PG_PASSWORD = os.environ.get('PG_DEV_PASSWORD', 'postgres')
    PG_DATABASE = os.environ.get('PG_DEV_DATABASE', 'postgres')
    PG_ENGINE_STR = f'postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'

else:
    PG_HOST = os.environ.get('PG_DEV_HOST', 'db')
    PG_PORT = os.environ.get('PG_DEV_PORT', '5432')
    PG_USER = os.environ.get('PG_DEV_USER', 'postgres')
    PG_PASSWORD = os.environ.get('PG_DEV_PASSWORD', 'postgres')
    PG_DATABASE = os.environ.get('PG_DEV_DATABASE', 'postgres')
    PG_ENGINE_STR = f'postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'

pg_engine = create_async_engine(
    PG_ENGINE_STR,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False,
)
