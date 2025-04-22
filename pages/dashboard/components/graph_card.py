import dash_mantine_components as dmc 
from dash.development.base_component import Component
from dash.dcc import Graph


def create_graph_card_wrapper(graph: Graph, title: str, menu: Component = None):
    return dmc.Paper(
        children=dmc.Stack([
            dmc.Group([dmc.Title(title, order=3), menu], justify='space-between', align='center'),
            dmc.Divider(h=5),
            graph   
        ], m='md'),
        withBorder=True,
        # p='md'
    )