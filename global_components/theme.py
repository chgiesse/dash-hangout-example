from utils.helpers import get_theme_template

import dash_mantine_components as dmc 
from typing import Literal
from dash_iconify import DashIconify
from flash import clientside_callback, Input, callback, Output, Patch


shadcn_gray = [
    "#030712",
    "#111827",
    "#1f2937",
    "#374151",
    "#4b5563",
    "#6b7280",
    "#9ca3af",
    "#e5e7eb",
    "#f3f4f6",
    "#f9fafb",
]
shadcn_slate = [
    "#020617",
    "#0f172a",
    "#1e293b",
    "#334155",
    "#475569",
    "#64748b",
    "#94a3b8",
    "#e2e8f0",
    "#f1f5f9",
    "#f8fafc",
]
mantine_dark = [
    "#d3d4d6",
    "#7a7e83",
    "#383e46",
    "#4a5d79",
    "#222831",
    "#1f242c",
    "#181c22",
    "#0e1014",
    "#14181d",
    "#1b2027",
]

theme_type = Literal['plotly_dark', 'plotly']

class ThemeComponent(dmc.Switch):

    class ids:
        toggle = "color-scheme-toggle"
    
    base_colors_scheme = "light"

    theme_csc = clientside_callback(
        """ 
        (switchOn) => {
            const theme = switchOn ? 'dark' : 'light'
            document.documentElement.setAttribute('data-mantine-color-scheme', theme);  
        }
        """,
        Input(ids.toggle, "checked"),
    )

    @classmethod
    def graph_theme_callback(cls, graph_id: str):
        @callback(
            Output(graph_id, 'figure', allow_duplicate=True),
            Input(cls.ids.toggle, 'checked'),
            prevent_initial_call=True
        )

        def update_graph_template(is_darkmode: bool):   
            template = get_theme_template(is_darkmode)
            print("TEMPLATE IN CALLBACK", template, flush=True)
            figure = Patch()
            figure.layout.template = template
            return figure


    theme = {
        "primaryColor": "violet",
        "primareShade": "3",
        "defaultRadius": "md",  
        "components": {"Card": {"defaultProps": {"shadow": "sm"}}},
        "focusRing": "never",
        "colors": {"dark": mantine_dark, "slate": list(reversed(shadcn_slate))},
    }

    def __init__(self) -> None:
        super().__init__(
            mt="auto",
            offLabel=DashIconify(
                icon="line-md:sun-rising-loop", 
                width=15, 
                color=dmc.DEFAULT_THEME["colors"]["yellow"][8],
                id='temp2'
            ),
            onLabel=DashIconify(
                icon="line-md:moon-rising-alt-loop",
                width=15,
                color=dmc.DEFAULT_THEME["colors"]["yellow"][6],
                id='temp1'
            ),
            id=self.ids.toggle,
            persistence=True,
            color="grey",
        )