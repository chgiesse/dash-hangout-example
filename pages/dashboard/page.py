from utils.helpers import get_theme_template, get_icon
from .components.actionbar import ActionBar
from .components.figures import CategoryRankGraph, TotalSalesGraph, TotalSentimentGraph
from .components.menu import GraphDownload
from .components.graph_card import create_total_sales_card
from .models import AmazonQueryParams, SalesCallbackParams
from .api import get_category_ranks, get_total_sales, get_total_sentiment, get_avg_rating, get_product_metrics

from flash import register_page
from functools import partial
from pydantic import ValidationError
import dash_mantine_components as dmc
import asyncio 

register_page(__name__, path='/dashboard', title='Dashboard')

async def layout(**kwargs):
    try:
        filters = AmazonQueryParams(**kwargs)
        is_darkmode = bool(kwargs.pop('theme', True))
        is_single_view = len(filters.categories) == 1

    except ValidationError as e:
        return dmc.Alert(
            color='red',    
            icon=get_icon('material-symbols:error-outline-rounded'),
            title='Validation Error',
            children=str(e)
        )

    rank_source, rank_component = (
        (
            get_product_metrics(filters=filters),
            partial(create_total_sales_card, category=filters.categories[0])
        )
        if is_single_view else
        (
            get_category_ranks(filters=filters, variant=SalesCallbackParams.get_default_variant()),
            partial(CategoryRankGraph, is_darkmode=is_darkmode)
        )
    )

    (
        rank_data,
        total_sales,
        total_sentiment,
        avg_rating
    ) = await asyncio.gather(
        rank_source,
        get_total_sales(filters=filters, variant=SalesCallbackParams.get_default_variant()),
        get_total_sentiment(filters=filters),   
        get_avg_rating(filters=filters),
        return_exceptions=True
    )
    
    return [
        GraphDownload(),
        dmc.Grid(
            children=[
                dmc.GridCol(
                    span=9,
                    children=dmc.Grid([
                        dmc.GridCol(
                            rank_component(rank_data), 
                            span=12 if is_single_view else 4
                        ),
                        dmc.GridCol(
                            TotalSalesGraph(total_sales, is_darkmode), 
                            span=12 if is_single_view else 8
                        ),
                        dmc.GridCol(
                            TotalSentimentGraph(total_sentiment, avg_rating, is_darkmode), 
                            span=12
                        ),
                    ]),
                ),
                dmc.GridCol(
                    span=3,
                    pos='sticky',
                    top=0,
                    h='calc(100vh - var(--mantine-spacing-xl))',
                    bg='var(--mantine-color-body)',
                    children=[
                        dmc.Title('Example Dashboard', order=2, ml='md'),
                        ActionBar(filters)
                    ],
                ),
            ]
        )
    ]