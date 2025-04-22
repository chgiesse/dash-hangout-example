from utils.helpers import get_theme_template
from .components.actionbar import ActionBar
from .components.figures import CategoryRankGraph, TotalSalesGraph
from .components.menu import GraphDownload
from .models import AmazonQueryParams, SalesCallbackParams
from .api import get_category_ranks, get_total_sales

from flash import register_page
import dash_mantine_components as dmc
import asyncio 

register_page(__name__, path='/dashboard', title='Dashboard')

async def layout(**kwargs):
    is_darkmode = kwargs.pop('theme', 'plotly')
    template = get_theme_template(is_darkmode)
    filters = AmazonQueryParams(**kwargs)
    (
        cat_rank,
        total_sales
    ) = await asyncio.gather(
        get_category_ranks(filters=filters, sales_params=SalesCallbackParams()),
        get_total_sales(filters=filters, sales_params=SalesCallbackParams()),

    )
    
    return [
        GraphDownload(),
        dmc.Grid(
            children=[
                dmc.GridCol(
                    children=dmc.Grid([
                        dmc.GridCol(CategoryRankGraph(cat_rank, template), span=4),
                        dmc.GridCol(TotalSalesGraph(total_sales, template), span=8),
                    ]),
                    span=9
                ),
                dmc.GridCol(
                    [
                        dmc.Title('Example Dashboard', order=2, ml='md'),
                        ActionBar(filters)
                    ],
                    span=3,
                ),
            ]
        )
    ]