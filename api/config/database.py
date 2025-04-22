from sqlalchemy.exc import OperationalError, InterfaceError
from sqlalchemy.ext.asyncio import (
    async_sessionmaker, 
    AsyncSession, 
    create_async_engine
)

from dotenv import load_dotenv
from functools import wraps
from time import time
import asyncio
import os

load_dotenv()

# PostgreSQL connection details
PG_HOST = os.environ.get('PG_HOST', 'localhost')
PG_PORT = os.environ.get('PG_PORT', '5432')
PG_USER = os.environ.get('PG_USER', 'postgres')
PG_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
PG_DATABASE = os.environ.get('PG_DATABASE', 'postgres')
PG_ENGINE_STR = f'postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'

pg_engine = create_async_engine(
    PG_ENGINE_STR,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False,
)

engine_map = {
    'dash_example': pg_engine
}

def create_session(engine):
    session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
    )
    return session_maker


def db_operator(
    timeout: int = 1, 
    max_retries: int = 3, 
    database: str = 'dash_example', 
    verbose: bool = False
    ):
    """Decorator to handle database operations with retry logic."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            engine = engine_map.get(database)
            if not engine:
                raise Exception(f'DB: {database} is not a valid database')

            session_maker = create_session(pg_engine)
            attempts = 0
            start_time = time()
            while attempts <= max_retries:
                async with session_maker() as db:
                    try:
                        result = await func(db, *args, **kwargs)
                        if verbose:
                            time_elapsed = time() - start_time
                            print(
                                f'Function {func.__name__} finished in {time_elapsed:.2f} seconds after {attempts} attempts.',
                                flush=True,
                            )
                        return result
                    except (OperationalError, InterfaceError) as exc:
                        attempts += 1
                        time_elapsed = time() - start_time
                        print(
                            f'Function {func.__name__} failed after {time_elapsed:.2f} seconds and {attempts} attempts: {exc}',
                            flush=True,
                        )
                        await asyncio.sleep(timeout)
                        if attempts > max_retries:
                            raise 
        return wrapper
    return decorator