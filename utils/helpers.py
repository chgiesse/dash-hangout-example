import dash_mantine_components as dmc 
from dash_iconify import DashIconify
from urllib.parse import parse_qs as base_parse_qs


def get_icon(icon: str, height: int = 20, *args, **kwargs):
    return DashIconify(icon=icon, height=height, *args, **kwargs)


def create_navlink(href: str, icon: str, title: str, *args, **kwargs):
    return dmc.Anchor(
        [
            dmc.Text(title, fw=700),
            dmc.ActionIcon(get_icon(icon, height=25), size="xl", variant="subtle")
        ],
        href=href,
        *args,
        **kwargs,
    )

def parse_qs(query_string, *args, **kwargs):
    query_string = query_string.split('?')[-1]
    parsed = base_parse_qs(query_string, *args, **kwargs)
    return {key: values[0] if values else '' for key, values in parsed.items()}


def get_theme_template(is_darkmode: bool):
    return 'plotly_dark' if is_darkmode else 'plotly'