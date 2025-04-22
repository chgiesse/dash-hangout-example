from .config.database import db_operator
from .models.amazon import AmazonProduct, Base

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import pandas as pd


@db_operator()
async def setup_db(db: AsyncSession):
    data = pd.read_csv('assets/datasets/amazon_processed.csv')
    data.SaleDate = pd.to_datetime(data.SaleDate)
    await db.execute(text('CREATE SCHEMA IF NOT EXISTS "AnalyticsDM"'))
    await db.commit()
    await db.execute(text('CREATE SCHEMA IF NOT EXISTS "AnalyticsDM"'))
    await db.commit()
    await db.run_sync(lambda sync_session: Base.metadata.create_all(sync_session.bind))

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

    