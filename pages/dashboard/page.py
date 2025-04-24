from utils.helpers import get_theme_template, get_icon
from .components.actionbar import ActionBar
from .components.figures import CategoryRankGraph, TotalSalesGraph, TotalSentimentGraph
from .components.menu import GraphDownload
from .models import AmazonQueryParams, SalesCallbackParams
from .api import get_category_ranks, get_total_sales, get_total_sentiment, get_avg_rating

from flash import register_page
from pydantic import ValidationError
import dash_mantine_components as dmc
import asyncio 

register_page(__name__, path='/dashboard', title='Dashboard')

async def layout(**kwargs):
    try:
        filters = AmazonQueryParams(**kwargs)
    except ValidationError as e:
        return dmc.Alert(
            color='red',
            icon=get_icon('material-symbols:error-outline-rounded'),
            title='Validation Error',
            children=str(e)
        )

    (
        cat_rank,
        total_sales,
        total_sentiment,
        avg_rating
    ) = await asyncio.gather(
        get_category_ranks(filters=filters, sales_params=SalesCallbackParams()),
        get_total_sales(filters=filters, sales_params=SalesCallbackParams()),
        get_total_sentiment(filters=filters),   
        get_avg_rating(filters=filters)
    )
    
    is_darkmode = kwargs.pop('theme', 'plotly')
    template = get_theme_template(is_darkmode)
    
    return [
        GraphDownload(),
        dmc.Grid(
            children=[
                dmc.GridCol(
                    children=dmc.Grid([
                        dmc.GridCol(CategoryRankGraph(cat_rank, template), span=4),
                        dmc.GridCol(TotalSalesGraph(total_sales, template), span=8),
                        dmc.GridCol(TotalSentimentGraph(total_sentiment, avg_rating, template), span=12),
                    ]),
                    span=9
                ),
                dmc.GridCol(
                    [
                        dmc.Title('Example Dashboard', order=2, ml='md'),
                        ActionBar(filters)
                    ],
                    span=3,
                    style={
                        'position': 'sticky',
                        'top': 0,
                        'height': 'calc(100vh - var(--mantine-spacing-xl))'
                    }
                ),
            ]
        )
    ]