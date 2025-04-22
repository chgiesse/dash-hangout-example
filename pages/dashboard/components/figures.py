from global_components.notifications import NotificationsContainer
from global_components.theme import ThemeComponent, theme_type
from utils.helpers import parse_qs, get_theme_template
from utils.constants import common_figure_config
from ..api import get_category_ranks, get_total_sales
from ..models import AmazonQueryParams, SalesCallbackParams, sales_variant_type
from .graph_card import create_graph_card_wrapper
from .switch import create_agg_switch
from .menu import GraphMenu

from pydantic import ValidationError
from flash import callback, Input, Output, State, set_props, no_update, ctx
import dash_mantine_components as dmc 
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
import pandas as pd


class CategoryRankGraph(dmc.Box):

    title = 'Top Categories'

    class ids:
        graph = 'amazon-top-category-graphs'
        relative_switch = 'amazon-top-category-rel-switch'
        variant_select = 'amazon-top-category-var-select'
    
    GraphMenu.download_callback(ids.graph)
    ThemeComponent.graph_theme_callback(ids.graph)

    @callback(
        Output(ids.graph, 'figure'),
        Input(ids.relative_switch, 'checked'),
        Input(ids.variant_select, 'value'),
        State('_pages_location', 'search'),
        prevent_initial_call=True
    )
    async def update(is_relative: bool, variant: str, qs: str):
        try:
            query_params = parse_qs(qs)
            filters = AmazonQueryParams(**query_params)
            sales_params = SalesCallbackParams(variant=variant, is_relative=is_relative)
        except ValidationError as e:
            set_props(
                NotificationsContainer.ids.container, 
                {
                    'children': dmc.Notification(
                        title='Validation Error',
                        message=str(e),
                        color='red',
                        action='show'
                    )
                }
            )
            return no_update
        
        data = await get_category_ranks(filters=filters, sales_params=sales_params)
        if is_relative:
            data.ProductCount = data.ProductCount / data.ProductCount.sum()
        
        fig = CategoryRankGraph.figure(data, is_relative=is_relative)
        return fig


    @staticmethod
    def figure(data: pd.DataFrame, is_relative: bool = False):

        if is_relative:
            common_props = dict(
                values=data.ProductCount,
                labels=data.MainCategory,
                hole=0.6,
                textfont=dict(size=10)
            )

            fig1 = go.Pie(**common_props, textinfo="percent", textposition="inside")

            fig2 = go.Pie(
                **common_props,
                textinfo="label",
                textposition="outside",
            )
            fig = go.Figure([fig2, fig1])
            fig.update_layout(margin=dict(l=100, r=80, t=40, b=40))
        
        else:
            fig = px.bar(
                data, 
                x='ProductCount', 
                y='MainCategory', 
                orientation='h', 
                color='MainCategory',
                text_auto=True
            )
            
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

        fig.update_layout(**common_figure_config, showlegend=False)
        return fig


    def __init__(self, data: pd.DataFrame, theme: theme_type):
        fig = self.figure(data)
        fig.update_layout(template=theme)
        super().__init__(
            create_graph_card_wrapper(
                graph=dcc.Graph(
                    figure=fig, 
                    config={'displayModeBar': False},
                    id=self.ids.graph
                ),
                title=self.title,
                menu=dmc.Group([
                    dmc.Select(
                        data=[{'value': val, 'label': val.title()} for val in SalesCallbackParams.get_variants()],
                        placeholder='variant',
                        size='sm',
                        w=120,
                        id=self.ids.variant_select,
                        value=SalesCallbackParams.get_default_variant(),
                        clearable=False,
                        allowDeselect=False
                    ),
                    GraphMenu(
                        graph_id=self.ids.graph,
                        aggregation_items=[create_agg_switch(self.ids.relative_switch)]
                    )
                ])
            ),
        )


class TotalSalesGraph(dmc.Box):

    title = 'Total Sales over Time'

    class ids:
        graph = 'amazon-total-sales-graphs'
        relative_switch = 'amazon-total-sales-rel-switch'
        running_switch = 'amazon-total-sales-run-switch'
        variant_select =  'amazon-total-sales-var-select'
    
    GraphMenu.download_callback(ids.graph)
    ThemeComponent.graph_theme_callback(ids.graph)

    @callback(
        Output(ids.graph, 'figure'),
        Input(ids.relative_switch, 'checked'),
        Input(ids.running_switch, 'checked'),
        Input(ids.variant_select, 'value'),
        State('_pages_location', 'search'),
        State(ThemeComponent.ids.toggle, 'checked'),
        prevent_initial_call=True
    )
    async def update(is_relative: bool, is_running: bool, variant: sales_variant_type, qs: str, is_dark: bool):
        try:
            query_params = parse_qs(qs)
            filters = AmazonQueryParams(**query_params)
            sales_params = SalesCallbackParams(
                variant=variant, 
                is_relative=is_relative, 
                is_running=is_running
            )
        
        except ValidationError as e:
            set_props(
                NotificationsContainer.ids.container, 
                {
                    'children': dmc.Notification(
                        title='Validation Error',
                        message=str(e),
                        color='red',
                        action='show'
                    )
                }
            )
            return no_update
        
        triggered_id = ctx.triggered_id
        template = get_theme_template(is_dark)
        data = await get_total_sales(filters=filters, sales_params=sales_params)

        if is_relative and triggered_id == TotalSalesGraph.ids.relative_switch:
            data = data.divide(data.sum(axis=1), axis=0).round(3).fillna(0)
        
        if is_running and triggered_id == TotalSalesGraph.ids.running_switch:
            data = data.cumsum()
        
        fig = TotalSalesGraph.figure(data)
        fig.update_layout(template=template)
        return fig

    @staticmethod
    def figure(data: pd.DataFrame):
        fig = px.bar(data, text_auto=True)
        fig.update_layout(
            **common_figure_config, 
            margin=dict(l=0, r=0, t=0, b=0),
            uirevision=True,

        )
        return fig

    def __init__(self, data: pd.DataFrame, theme: theme_type):
        fig = self.figure(data)
        fig.update_layout(template=theme)
        super().__init__(
            create_graph_card_wrapper(
                graph=dcc.Graph(
                    figure=fig, 
                    config={'displayModeBar': False},
                    id=self.ids.graph
                ),
                title=self.title,
                menu=dmc.Group([
                    dmc.Select(
                        data=[{'value': val, 'label': val.title()} for val in SalesCallbackParams.get_variants()],
                        placeholder='variant',
                        size='sm',
                        w=120,
                        id=self.ids.variant_select,
                        value=SalesCallbackParams.get_default_variant(),
                        clearable=False,
                        allowDeselect=False
                    ),
                    GraphMenu(
                        graph_id=self.ids.graph,
                        aggregation_items=[
                            create_agg_switch(self.ids.relative_switch),
                            create_agg_switch(self.ids.running_switch, title='Running'),
                        ]
                    )
                ])
            )
        )