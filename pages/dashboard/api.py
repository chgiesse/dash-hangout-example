from api.config.database import db_operator
from api.models.amazon import AmazonProduct
from .models import AmazonQueryParams, SalesCallbackParams, sales_variant_type, granularity_type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, literal, String
from sqlalchemy.orm import Query
import pandas as pd
import asyncio


def apply_amazon_filters(query: Query, filters: AmazonQueryParams):
    if len(filters.categories) > 0:
        query = query.filter(AmazonProduct.MainCategory.in_(filters.categories))
    
    if date_range := filters.sale_date_range:
        query = query.filter(AmazonProduct.SaleDate.between(cleft=date_range[0], cright=date_range[1]))
    
    if rating := filters.rating_range:
        query = query.filter(AmazonProduct.Rating.between(cleft=rating[0], cright=rating[1]))

    return query


def get_agg_variant_column(agg_variant: sales_variant_type):
    if agg_variant == 'amount':
        return func.count(AmazonProduct.ProductId)

    if agg_variant == 'discount':
        return func.avg(AmazonProduct.DiscountPercentage)

    if agg_variant == 'price':
        return func.sum(AmazonProduct.ActualPrice)
    

def get_date_granularity_column(granularity: granularity_type, date_column):

    if granularity == 'day':
        return func.to_char(date_column, 'YYYY-MM-DD'), 'date'
    elif granularity == 'month':
        return func.to_char(date_column, 'YYYY-MM'), 'month'
    elif granularity == 'year':
        return func.to_char(date_column, 'YYYY'), 'year'
    else:
        return func.to_char(date_column, 'YYYY-MM'), 'month'


@db_operator(timeout=.5, max_retries=3, verbose=True)
async def get_category_ranks(db: AsyncSession, filters: AmazonQueryParams, sales_params: SalesCallbackParams):
    agg_col = get_agg_variant_column(sales_params.variant)
    query = select(
        AmazonProduct.MainCategory
        , agg_col.label('ProductCount')
    )

    query = apply_amazon_filters(query, filters)
    query = query.group_by(AmazonProduct.MainCategory)
    query = query.order_by(desc('ProductCount'))
    result = await db.execute(query)
    return pd.DataFrame(result) 


@db_operator(verbose=True)
async def get_total_sales(db: AsyncSession, filters: AmazonQueryParams, sales_params: SalesCallbackParams):
    agg_col = get_agg_variant_column(sales_params.variant)
    date_col, _ = get_date_granularity_column(filters.granularity, AmazonProduct.SaleDate)
    query = select(
        AmazonProduct.MainCategory
        , date_col.label('Date')
        , agg_col.label('ProductCount')
    )

    query = apply_amazon_filters(query, filters)
    query = query.group_by(date_col, AmazonProduct.MainCategory)
    query = query.order_by(desc('ProductCount'))
    result = await db.execute(query)
    data = pd.DataFrame(result)
    data = data.pivot(index='Date', columns='MainCategory', values='ProductCount')
    data.fillna(0)
    return data

@db_operator(verbose=True)
async def get_total_sentiment(db: AsyncSession, filters: AmazonQueryParams):
    date_col, _ = get_date_granularity_column(filters.granularity, AmazonProduct.SaleDate)
    query = select(
            date_col.label('Date')
            , AmazonProduct.ReviewSentiment
            , func.count(AmazonProduct.ProductId).label('ProductCount')
        )
    
    query = apply_amazon_filters(query, filters)
    query = query.group_by(date_col, AmazonProduct.ReviewSentiment)
    result = await db.execute(query)

    data = pd.DataFrame(result)
    data = data.pivot(columns='ReviewSentiment', index='Date', values='ProductCount')
    data = data.fillna(0)
    return data 


@db_operator(verbose=True)
async def get_avg_rating(db: AsyncSession, filters: AmazonQueryParams):
    date_col, _ = get_date_granularity_column(filters.granularity, AmazonProduct.SaleDate)
    query = select(
        date_col.label('Date')
        , func.avg(AmazonProduct.Rating).label('AvgRating')
    )
    
    query = apply_amazon_filters(query, filters)
    query = query.group_by(date_col)
    result = await db.execute(query)
    data = pd.DataFrame(result)
    print('DAta: ', query, flush=True)
    data.set_index('Date', inplace=True)
    data.sort_index(ascending=True, inplace=True)
    return data