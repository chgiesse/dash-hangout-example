from global_components.notifications import NotificationsContainer
from global_components.theme import ThemeComponent, theme_type
from global_components.location import Url
from utils.helpers import parse_qs, get_theme_template
from utils.constants import common_figure_config
from ..api import get_category_ranks, get_total_sales, get_avg_rating, get_total_sentiment
from ..models import AmazonQueryParams, SalesCallbackParams, sales_variant_type
from .graph_card import create_graph_card_wrapper
from .switch import create_agg_switch
from .menu import GraphMenu

from pydantic import ValidationError
from flash import callback, Input, Output, State, no_update, ctx, clientside_callback
from dash_ag_grid import AgGrid
import dash_mantine_components as dmc 
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from dash import dcc
import pandas as pd
import asyncio


class CategoryRankGraph(dmc.Box):

    title = 'Top Categories'

    class ids:
        graph = 'amazon-top-category-graphs'
        relative_switch = 'amazon-top-category-rel-switch'
        variant_select = 'amazon-top-category-var-select'
    
    GraphMenu.download_callback(ids.graph)
    # ThemeComponent.graph_theme_callback(ids.graph)

    @callback(
        Output(ids.graph, 'figure'),
        Input(ids.relative_switch, 'checked'),
        Input(ids.variant_select, 'value'),
        State(ThemeComponent.ids.toggle, 'checked'),
        State(Url.ids.location, 'search'),
        prevent_initial_call=True
    )
    async def update(is_relative: bool, variant: str, is_darkmode: bool, qs: str):
        try:
            query_params = parse_qs(qs)
            filters = AmazonQueryParams(**query_params)
            sales_params = SalesCallbackParams(variant=variant, is_relative=is_relative)

        except ValidationError as e:
            NotificationsContainer.send_notification(
                title='Validation Error',
                message=str(e),
                color='red',
            )
            return no_update

        data = await get_category_ranks(filters=filters, variant=sales_params.variant)

        if is_relative:
            data.ProductCount = data.ProductCount / data.ProductCount.sum()
        
        fig = CategoryRankGraph.figure(data, is_relative=is_relative, is_darkmode=is_darkmode)

        return fig


    @staticmethod
    def figure(data: pd.DataFrame, is_relative: bool = False, is_darkmode: bool = False):
        template = get_theme_template(is_darkmode)

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
            fig.update_layout(
                margin=dict(l=100, r=80, t=40, b=40),
            )
        
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

        fig.update_layout(**common_figure_config, showlegend=False, template=template)
        return fig


    def __init__(self, data: pd.DataFrame, is_darkmode: bool):
        fig = self.figure(data, is_darkmode=is_darkmode)

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
        graph = 'amazon-total-sales-graph'
        table = 'amazon-total-sales-table'
        relative_switch = 'amazon-total-sales-rel-switch'
        table_switch = 'amazon-total-sales-tbl-switch'
        running_switch = 'amazon-total-sales-run-switch'
        variant_select =  'amazon-total-sales-var-select'

    
    GraphMenu.download_callback(ids.graph)
    # ThemeComponent.graph_theme_callback(ids.graph)
    clientside_callback(
        f'''( hideTable ) => {{
            document.querySelector('.{ids.table}').setAttribute('data-hidden', !hideTable);
            document.querySelector('.{ids.graph}').setAttribute('data-hidden', hideTable);
        }}''',
        Input(ids.table_switch, 'checked'),
    )

    @callback(
        Output(ids.graph, 'figure'),
        Output(ids.table, 'rowData'),
        Input(ids.relative_switch, 'checked'),
        Input(ids.running_switch, 'checked'),
        Input(ids.variant_select, 'value'),
        State(Url.ids.location, 'search'),
        State(ThemeComponent.ids.toggle, 'checked'),
        prevent_initial_call=True
    )
    async def update(is_relative: bool, is_running: bool, variant: sales_variant_type, qs: str, is_darkmode: bool):
        try:
            query_params = parse_qs(qs)
            filters = AmazonQueryParams(**query_params)
            sales_params = SalesCallbackParams(
                variant=variant, 
                is_relative=is_relative, 
                is_running=is_running
            )
        
        except ValidationError as e:
            NotificationsContainer.send_notification(
                title='Validation Error',
                message=str(e),
                color='red',
            )
            return no_update
        
        triggered_id = ctx.triggered_id
        data = await get_total_sales(filters=filters, variant=sales_params.variant)

        if is_relative and triggered_id == TotalSalesGraph.ids.relative_switch:
            data = data.divide(data.sum(axis=1), axis=0).round(3).fillna(0)
        
        if is_running and triggered_id == TotalSalesGraph.ids.running_switch:
            data = data.cumsum()
        
        fig = TotalSalesGraph.figure(data, is_darkmode)
        row_data = data.T.reset_index(names='Category').to_dict(orient='records')

        return fig, row_data    

    @staticmethod
    def figure(data: pd.DataFrame, is_darkmode: bool):
        fig = px.bar(data, text_auto=True)
        template = get_theme_template(is_darkmode)
        fig.update_layout(
            **common_figure_config, 
            margin=dict(l=0, r=0, t=0, b=0),
            uirevision=True,
            template=template

        )
        return fig

    @classmethod
    def table(cls, data: pd.DataFrame):
        data = data.T.reset_index(names='Category')
        columnDefs = [{'field': 'Category', 'pinned': 'left', 'width': 180, 'filter': True}]
        columnDefs += [{'field': col, 'width': 110, 'filter': False} for col in data.columns[1:]]

        table = AgGrid(
            id=cls.ids.table,
            rowData=data.to_dict(orient='records'),
            columnDefs=columnDefs,
            defaultColDef={"filter": False},
            className='ag-theme-quartz-auto-dark card-bg',
            dashGridOptions = {"rowHeight": 55},
        )
        return table


    def __init__(self, data: pd.DataFrame, is_darkmode: bool):
        fig = self.figure(data, is_darkmode)
        graph = dcc.Graph(
            figure=fig, 
            config={'displayModeBar': False},
            id=self.ids.graph
        )
        table = self.table(data)

        graph_container = dmc.Box(
            children=[
                dmc.Center(
                    table, 
                    className=self.ids.table, 
                    **{'data-hidden': True}, 
                ),
                dmc.Box(
                    graph, 
                    className=self.ids.graph, 
                    **{'data-hidden': False}
                ),
            ], 
        )

        super().__init__(
            create_graph_card_wrapper(
                graph=graph_container,
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
                        ],
                        application_items=[create_agg_switch(self.ids.table_switch, title='Table view')]
                    )
                ])
            )
        )


class TotalSentimentGraph(dmc.Box):

    title = 'Sentiment and Rating over Time'
    class ids:
        graph = 'amazon-total-sentiment-graph'
        relative_switch = 'amazon-total-sentiment-rel-switch'

    @callback(
        Output(ids.graph, 'figure'),
        Input(ids.relative_switch, 'checked'),
        State(Url.ids.location, 'search'),
        State(ThemeComponent.ids.toggle, 'checked'),
        prevent_initial_call=True
    )
    async def update(is_relative: bool, qs: str, is_darkmode: bool):
        try:
            query_params = parse_qs(qs)
            filters = AmazonQueryParams(**query_params)
        
        except ValidationError as e:
            NotificationsContainer.send_notification(
                title='Validation Error',
                message=str(e),
                color='red',
            )
            return 

        sentiment_data, rating_data = await asyncio.gather(
            get_total_sentiment(filters=filters), 
            get_avg_rating(filters=filters)
        )
        
        if is_relative:
            sentiment_data = sentiment_data.divide(sentiment_data.sum(axis=1), axis=0).round(3)

        fig = TotalSentimentGraph.figure(sentiment_data, rating_data, is_darkmode)
        return fig

    @staticmethod
    def figure(sentiment_data: pd.DataFrame, rating_data: pd.DataFrame, is_darkmode: bool = False):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        template = get_theme_template(is_darkmode)

        for sentiment in sentiment_data.columns:
            fig.add_trace(
                go.Bar(
                    x=sentiment_data.index,
                    y=sentiment_data[sentiment],
                    name=f"{sentiment}",
                    text=sentiment_data[sentiment],
                    textposition='auto'
                ),
                secondary_y=False
            )

        fig.add_trace(
            go.Scatter(
                x=rating_data.index,
                y=rating_data.AvgRating.values,
                name="Average Rating",
                line=dict(color='red', width=3),
                mode='lines+markers',
            ),
            secondary_y=True
        )

        fig.update_layout(
            barmode='stack',
            template=template,
            **common_figure_config
        )

        fig.update_yaxes(title_text="Sentiment classification", secondary_y=False)
        fig.update_yaxes(
            title_text="Average Rating", 
            secondary_y=True,
            range=[1, 5],
        )
        return fig 


    def __init__(self, sentiment_data: pd.DataFrame, rating_data: pd.DataFrame, is_darkmode: bool):
        fig = self.figure(sentiment_data, rating_data, is_darkmode)
        super().__init__(
            create_graph_card_wrapper(
                graph=dcc.Graph(
                    figure=fig,
                    id=self.ids.graph,
                    config={'displayModeBar': False},
                ),
                title=self.title,
                menu=GraphMenu(
                    graph_id=self.ids.graph,
                    aggregation_items=[create_agg_switch(self.ids.relative_switch)]
                )
            )
        )