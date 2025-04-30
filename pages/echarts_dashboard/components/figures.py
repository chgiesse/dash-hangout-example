# from global_components.notifications import NotificationsContainer
# from global_components.theme import ThemeComponent, theme_type
# from utils.helpers import parse_qs, get_theme_template
# from utils.constants import common_figure_config

# from ...dashboard.api import get_category_ranks, get_total_sales, get_avg_rating, get_total_sentiment
# from ...dashboard.models import AmazonQueryParams, SalesCallbackParams, sales_variant_type
# from ...dashboard.components.graph_card import create_graph_card_wrapper
# from ...dashboard.components.switch import create_agg_switch
# from ...dashboard.components.menu import GraphMenu

# from pydantic import ValidationError
# from flash import callback, Input, Output, State, set_props, no_update, ctx, clientside_callback
# from dash_ag_grid import AgGrid
# import dash_mantine_components as dmc 
# from flash_echarts import FlashAdvancedEcharts
# from dash import dcc, html
# import pandas as pd
# import asyncio

# class CategoryRankGraph(dmc.Box):

#     title = 'Top Categories'

#     class ids:
#         graph = 'amazon-top-category-graphs'
#         relative_switch = 'amazon-top-category-rel-switch'
#         variant_select = 'amazon-top-category-var-select'
    
#     GraphMenu.download_callback(ids.graph)
#     ThemeComponent.echarts_theme_callback(ids.graph)

#     @callback(
#         Output(ids.graph, 'option'),
#         Input(ids.relative_switch, 'checked'),
#         Input(ids.variant_select, 'value'),
#         State(ThemeComponent.ids.toggle, 'checked'),
#         State('_pages_location', 'search'),
#         prevent_initial_call=True
#     )
#     async def update(is_relative: bool, variant: str, is_darkmode: bool, qs: str):
#         try:
#             query_params = parse_qs(qs)
#             filters = AmazonQueryParams(**query_params)
#             sales_params = SalesCallbackParams(variant=variant, is_relative=is_relative)
#         except ValidationError as e:
#             set_props(
#                 NotificationsContainer.ids.container, 
#                 {
#                     'children': dmc.Notification(
#                         title='Validation Error',
#                         message=str(e),
#                         color='red',
#                         action='show'
#                     )
#                 }
#             )
#             return no_update
        
#         data = await get_category_ranks(filters=filters, sales_params=sales_params)
#         if is_relative:
#             data.ProductCount = data.ProductCount / data.ProductCount.sum()
        
#         options = CategoryRankGraph.echarts_options(data, is_relative=is_relative)
#         return options


#     @staticmethod
#     def echarts_options(data: pd.DataFrame, is_relative: bool = False):
        
#         if is_relative:
#             # Pie chart for relative view
#             options = {
#                 'backgroundColor': 'transparent',
#                 'tooltip': {
#                     'trigger': 'item',
#                     'formatter': '{a} <br/>{b} : {c} ({d}%)'
#                 },
#                  'grid': {
#                     'left': '3%',
#                     'right': '4%',
#                     'bottom': '3%',
#                     'containLabel': True,
#                     'backgroundColor': 'transparent'
#                 },
#                 'series': [
#                     {
#                         'name': 'Categories',
#                         'type': 'pie',
#                         'radius': ['30%', '70%'],
#                         'center': ['50%', '50%'],
#                         'data': [{'value': float(v), 'name': k} for k, v in zip(data.MainCategory, data.ProductCount)],
#                         # 'emphasis': {
#                         #     'itemStyle': {
#                         #         'shadowBlur': 10,
#                         #         'shadowOffsetX': 0,
#                         #         'shadowColor': 'rgba(0, 0, 0, 0.5)'
#                         #     }
#                         # },
#                     }
#                 ]
#             }
#         else:
#             # Bar chart for absolute view
#             options = {
#                 'backgroundColor': 'transparent',
#                 'tooltip': {
#                     'trigger': 'axis',
#                     'axisPointer': {
#                         'type': 'shadow'
#                     }
#                 },
#                 'grid': {
#                     'left': '3%',
#                     'right': '4%',
#                     'bottom': '3%',
#                     'containLabel': True,
#                     'backgroundColor': 'transparent'
#                 },
#                 'xAxis': {
#                     'type': 'value',
#                     'boundaryGap': [0, 0.01]
#                 },
#                 'yAxis': {
#                     'type': 'category',
#                     'data': data.MainCategory.tolist()
#                 },
#                 'series': [
#                     {
#                         'name': 'Product Count',
#                         'type': 'bar',
#                         'data': data.ProductCount.tolist(),
#                         'label': {
#                             'show': True,
#                             'position': 'right'
#                         }
#                     }
#                 ]
#             }
        
#         return options


#     def __init__(self, data: pd.DataFrame, theme: theme_type):
#         theme = 'dark' if theme else 'light'
#         options = self.echarts_options(data)
        
#         super().__init__(
#             create_graph_card_wrapper(
#                 graph=FlashAdvancedEcharts(
#                     option=options,
#                     id=self.ids.graph,
#                     style={'width': '100%', 'height': '400px'},
#                     theme=theme
#                 ),
#                 title=self.title,
#                 menu=dmc.Group([
#                     dmc.Select(
#                         data=[{'value': val, 'label': val.title()} for val in SalesCallbackParams.get_variants()],
#                         placeholder='variant',
#                         size='sm',
#                         w=120,
#                         id=self.ids.variant_select,
#                         value=SalesCallbackParams.get_default_variant(),
#                         clearable=False,
#                         allowDeselect=False
#                     ),
#                     GraphMenu(
#                         graph_id=self.ids.graph,
#                         aggregation_items=[create_agg_switch(self.ids.relative_switch)]
#                     )
#                 ])
#             ),
#         )


# class TotalSalesGraph(dmc.Box):

#     title = 'Total Sales over Time'

#     class ids:
#         graph = 'amazon-total-sales-graph'
#         table = 'amazon-total-sales-table'
#         relative_switch = 'amazon-total-sales-rel-switch'
#         table_switch = 'amazon-total-sales-tbl-switch'
#         running_switch = 'amazon-total-sales-run-switch'
#         variant_select =  'amazon-total-sales-var-select'

    
#     GraphMenu.download_callback(ids.graph)
#     ThemeComponent.echarts_theme_callback(ids.graph)
#     clientside_callback(
#         f'''( hideTable ) => {{
#             document.querySelector('.{ids.table}').setAttribute('data-hidden', !hideTable);
#             document.querySelector('.{ids.graph}').setAttribute('data-hidden', hideTable);
#         }}''',
#         Input(ids.table_switch, 'checked'),
#         prevent_initial_call=True
#     )

#     @callback(
#         Output(ids.graph, 'option'),
#         Output(ids.table, 'rowData'),
#         Input(ids.relative_switch, 'checked'),
#         Input(ids.running_switch, 'checked'),
#         Input(ids.variant_select, 'value'),
#         State('_pages_location', 'search'),
#         State(ThemeComponent.ids.toggle, 'checked'),
#         prevent_initial_call=True
#     )
#     async def update(is_relative: bool, is_running: bool, variant: sales_variant_type, qs: str, is_dark: bool):
#         try:
#             query_params = parse_qs(qs)
#             filters = AmazonQueryParams(**query_params)
#             sales_params = SalesCallbackParams(
#                 variant=variant, 
#                 is_relative=is_relative, 
#                 is_running=is_running
#             )
        
#         except ValidationError as e:
#             set_props(
#                 NotificationsContainer.ids.container, 
#                 {
#                     'children': dmc.Notification(
#                         title='Validation Error',
#                         message=str(e),
#                         color='red',
#                         action='show'
#                     )
#                 }
#             )
#             return no_update
        
#         triggered_id = ctx.triggered_id
#         data = await get_total_sales(filters=filters, sales_params=sales_params)

#         if is_relative and triggered_id == TotalSalesGraph.ids.relative_switch:
#             data = data.divide(data.sum(axis=1), axis=0).round(3).fillna(0)
        
#         if is_running and triggered_id == TotalSalesGraph.ids.running_switch:
#             data = data.cumsum()
        
#         options = TotalSalesGraph.echarts_options(data)
#         row_data = data.T.reset_index(names='Category').to_dict(orient='records')
#         return options, row_data    

#     @staticmethod
#     def echarts_options(data: pd.DataFrame):
#         # Convert DataFrame to ECharts format
#         series = []
#         for column in data.columns:
#             series.append({
#                 'name': column,
#                 'type': 'bar',
#                 'stack': 'total',
#                 'data': data[column].tolist(),
#             })

#         print(series, flush=True)
        
#         options = {
#             'backgroundColor': 'transparent',
#             'tooltip': {
#                 'trigger': 'axis',
#                 'axisPointer': {
#                     'type': 'shadow'
#                 }
#             },
#             'legend': {
#                 'data': list(data.columns)
#             },
#             'grid': {
#                 'left': '3%',
#                 'right': '4%',
#                 'bottom': '3%',
#                 'containLabel': True,
#             },
#             'xAxis': {
#                 'type': 'category',
#                 'data': data.index.tolist()
#             },
#             'yAxis': {
#                 'type': 'value'
#             },
#             'series': series
#         }
        
#         return options

#     @classmethod
#     def table(cls, data: pd.DataFrame):
#         data = data.T.reset_index(names='Category')
#         columnDefs = [{'field': 'Category', 'pinned': 'left', 'width': 180, 'filter': True}]
#         columnDefs += [{'field': col, 'width': 110, 'filter': False} for col in data.columns[1:]]

#         table = AgGrid(
#             id=cls.ids.table,
#             rowData=data.to_dict(orient='records'),
#             columnDefs=columnDefs,
#             defaultColDef={"filter": False},
#             className='ag-theme-quartz-auto-dark card-bg',
#             dashGridOptions = {"rowHeight": 55},
#         )
#         return table


#     def __init__(self, data: pd.DataFrame, theme: theme_type):
#         theme = 'dark' if theme else 'light'
#         options = self.echarts_options(data)
        
#         graph = FlashAdvancedEcharts(
#             option=options,
#             id=self.ids.graph,
#             style={'width': '100%', 'height': '400px'},
#             theme=theme
#         )
        
#         table = self.table(data)

#         graph_container = dmc.Box(
#             children=[
#                 dmc.Center(
#                     table, 
#                     className=self.ids.table, 
#                     **{'data-hidden': True}, 
#                 ),
#                 dmc.Box(
#                     graph, 
#                     className=self.ids.graph, 
#                     **{'data-hidden': False}
#                 ),
#             ], 
#         )

#         super().__init__(
#             create_graph_card_wrapper(
#                 graph=graph_container,
#                 title=self.title,
#                 menu=dmc.Group([
#                     dmc.Select(
#                         data=[{'value': val, 'label': val.title()} for val in SalesCallbackParams.get_variants()],
#                         placeholder='variant',
#                         size='sm',
#                         w=120,
#                         id=self.ids.variant_select,
#                         value=SalesCallbackParams.get_default_variant(),
#                         clearable=False,
#                         allowDeselect=False
#                     ),
#                     GraphMenu(
#                         graph_id=self.ids.graph,
#                         aggregation_items=[
#                             create_agg_switch(self.ids.relative_switch),
#                             create_agg_switch(self.ids.running_switch, title='Running'),
#                         ],
#                         application_items=[create_agg_switch(self.ids.table_switch, title='Table view')]
#                     )
#                 ])
#             )
#         )


# class TotalSentimentGraph(dmc.Box):

#     title = 'Sentiment and Rating over Time'
#     class ids:
#         graph = 'amazon-total-sentiment-graph'
#         relative_switch = 'amazon-total-sentiment-rel-switch'

#     ThemeComponent.echarts_theme_callback(ids.graph)

#     @callback(
#         Output(ids.graph, 'option'),
#         Input(ids.relative_switch, 'checked'),
#         State('_pages_location', 'search'),
#         State(ThemeComponent.ids.toggle, 'checked'),
#         prevent_initial_call=True
#     )
#     async def update(is_relative: bool, qs: str, is_darkmode: bool):
#         try:
#             query_params = parse_qs(qs)
#             filters = AmazonQueryParams(**query_params)
        
#         except ValidationError as e:
#             set_props(
#                 NotificationsContainer.ids.container, 
#                 {
#                     'children': dmc.Notification(
#                         title='Validation Error',
#                         message=str(e),
#                         color='red',
#                         action='show'
#                     )
#                 }
#             )
#             return no_update

#         sentiment_data, rating_data = await asyncio.gather(
#             get_total_sentiment(filters=filters), 
#             get_avg_rating(filters=filters)
#         )
        
#         if is_relative:
#             sentiment_data = sentiment_data.divide(sentiment_data.sum(axis=1), axis=0).round(3)

#         options = TotalSentimentGraph.echarts_options(sentiment_data, rating_data)
#         return options

#     @staticmethod
#     def echarts_options(sentiment_data: pd.DataFrame, rating_data: pd.DataFrame):
#         # Create series for sentiment data
#         series = []
#         for column in sentiment_data.columns:
#             series.append({
#                 'name': column,
#                 'type': 'bar',
#                 'stack': 'total',
#                 'data': sentiment_data[column].tolist(),
#                 'label': {
#                     'show': True
#                 }
#             })
        
#         # Add series for rating data
#         series.append({
#             'name': 'Average Rating',
#             'type': 'line',
#             'yAxisIndex': 1,
#             'data': rating_data.AvgRating.tolist(),
#             'symbol': 'circle',
#             'symbolSize': 8,
#             'lineStyle': {
#                 'width': 3
#             },
#             'itemStyle': {
#                 'color': '#ff0000'  # Red color for the line
#             }
#         })
        
#         options = {
#             'backgroundColor': 'transparent',
#             'tooltip': {
#                 'trigger': 'axis',
#                 'axisPointer': {
#                     'type': 'cross'
#                 }
#             },
#             'legend': {
#                 'data': list(sentiment_data.columns) + ['Average Rating']
#             },
#             'grid': {
#                 'left': '3%',
#                 'right': '4%',
#                 'bottom': '3%',
#                 'containLabel': True,
#                 'backgroundColor': 'transparent'
#             },
#             'xAxis': {
#                 'type': 'category',
#                 'data': sentiment_data.index.tolist()
#             },
#             'yAxis': [
#                 {
#                     'type': 'value',
#                     'name': 'Sentiment',
#                 },
#                 {
#                     'type': 'value',
#                     'name': 'Average Rating',
#                     'min': 1,
#                     'max': 5,
#                     'interval': 1,
#                     'position': 'right'
#                 }
#             ],
#             'series': series
#         }
        
#         return options

#     def __init__(self, sentiment_data: pd.DataFrame, rating_data: pd.DataFrame, theme: theme_type):
#         theme = 'dark' if theme else 'light'
#         options = self.echarts_options(sentiment_data, rating_data)
        
#         super().__init__(
#             create_graph_card_wrapper(
#                 graph=FlashAdvancedEcharts(
#                     option=options,
#                     id=self.ids.graph,
#                     style={'width': '100%', 'height': '400px'},
#                     theme=theme
#                 ),
#                 title=self.title,
#                 menu=GraphMenu(
#                     graph_id=self.ids.graph,
#                     aggregation_items=[create_agg_switch(self.ids.relative_switch)]
#                 )
#             )
#         )