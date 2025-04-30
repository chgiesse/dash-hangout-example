from .config.postgres import pg_engine
from .models.amazon import AmazonProduct, Base as AmazonBase
from .models.events import Base as EventBase

from sqlalchemy.exc import OperationalError, InterfaceError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import (
    async_sessionmaker, 
    AsyncSession
)
from sqlalchemy import text
from functools import wraps
import pandas as pd
from time import time
import asyncio


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


@db_operator()
async def setup_db(db: AsyncSession):
    data = pd.read_csv('assets/datasets/amazon_processed.csv')
    data.SaleDate = pd.to_datetime(data.SaleDate)
    await db.execute(text('CREATE SCHEMA IF NOT EXISTS "AnalyticsDM"'))
    await db.execute(text('CREATE SCHEMA IF NOT EXISTS "EventsDM"'))
    await db.commit()
    await db.run_sync(lambda sync_session: AmazonBase.metadata.create_all(sync_session.bind))
    await db.run_sync(lambda sync_session: EventBase.metadata.create_all(sync_session.bind))

    products = []
    for _, row in data.iterrows():
        product = AmazonProduct(
            ProductId=row['ProductId'],
            ProductName=row['ProductName'],
            Category=row['Category'],
            MainCategory=row['MainCategory'],
            DiscountedPrice=row.get('DiscountedPrice', None),
            ActualPrice=row.get('ActualPrice', None),
            DiscountPercentage=row.get('DiscountPercentage', None),
            Rating=row['Rating'],
            RatingCount=row.get('RatingCount', None),
            RatingSentiment=row['RatingSentiment'],
            AboutProduct=row.get('AboutProduct', None),
            ReviewContent=row.get('ReviewContent', None),
            ReviewSentiment=row['ReviewSentiment'],
            ReviewTitle=row.get('ReviewTitle', None),
            ReviewId=row.get('ReviewId', None),
            UserId=row.get('UserId', None),
            UserName=row.get('UserName', None),
            SaleDate=row['SaleDate'],
            SaleMonth=str(row['SaleMonth']),
            ImgLink=row.get('ImgLink', None),
            ProductLink=row.get('ProductLink', None)
        )
        products.append(product)
    
    db.add_all(products)
    await db.commit()