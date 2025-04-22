from api.config.database import db_operator
from api.models.amazon import AmazonProduct
from .models import AmazonQueryParams, SalesCallbackParams, sales_variant_type, granularity_type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, literal, String
import pandas as pd


def apply_filters():
    pass


def get_agg_variant_column(agg_variant: sales_variant_type):
    if agg_variant == 'amount':
        return func.count(AmazonProduct.ProductId)

    if agg_variant == 'discount':
        return func.avg(AmazonProduct.DiscountPercentage)

    if agg_variant == 'price':
        return func.sum(AmazonProduct.ActualPrice)
    

def get_date_granularity_column(granularity, date_column):

    if granularity == 'day':
        return func.to_char(date_column, 'YYYY-MM-DD'), 'date'
    elif granularity == 'month':
        return func.to_char(date_column, 'YYYY-MM'), 'month'
    elif granularity == 'year':
        return func.to_char(date_column, 'YYYY'), 'year'
    else:
        # Default to monthly if not specified
        return func.to_char(date_column, 'YYYY-MM'), 'month'



@db_operator(timeout=.5, max_retries=3, verbose=True)
async def get_category_ranks(db: AsyncSession, filters: AmazonQueryParams, sales_params: SalesCallbackParams):
    agg_col = get_agg_variant_column(sales_params.variant)
    query = select(
        AmazonProduct.MainCategory
        , agg_col.label('ProductCount')
    )
    query = query.group_by(AmazonProduct.MainCategory)
    query = query.order_by(desc('ProductCount'))
    result = await db.execute(query)
    return pd.DataFrame(result) 


@db_operator(verbose=True)
async def get_total_sales(db: AsyncSession, filters: AmazonQueryParams, sales_params: SalesCallbackParams):
    agg_col = get_agg_variant_column(sales_params.variant)
    date_col, col_name = get_date_granularity_column(filters.granularity, AmazonProduct.SaleDate)
    query = select(
        AmazonProduct.MainCategory
        , date_col.label('Date')
        , agg_col.label('ProductCount')
    )
    query = query.group_by(date_col, AmazonProduct.MainCategory)
    query = query.order_by(desc('ProductCount'))
    result = await db.execute(query)
    data = pd.DataFrame(result)
    data = data.pivot(index='Date', columns='MainCategory', values='ProductCount')
    data.fillna(0)
    return data