import dash_mantine_components as dmc 
from dash.development.base_component import Component
from dash.dcc import Graph
import pandas as pd


def create_graph_card_wrapper(graph: Graph, title: str, menu: Component = None):
    return dmc.Paper(
        children=dmc.Stack([
            dmc.Group([dmc.Title(title, order=3), menu], justify='space-between', align='center'),
            dmc.Divider(h=5),
            graph   
        ], m='md'),
        withBorder=True,
    )


def create_total_sales_card(data: pd.DataFrame, category: str):

    create_card = lambda title, amount: dmc.Card(
        children=[
            dmc.Text(title, fw=700, size='xl'),
            dmc.Text(amount)
        ]
    )

    return dmc.Group(
        grow=True,
        children=[
            create_card('Category', category),
            create_card('Total Items', data.ProductCount),
            create_card('Total Amount', data.TotalPrice),
            create_card('Avg Discount', data.AvgDiscount),
        ]
    )