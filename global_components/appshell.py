from utils.helpers import get_icon, create_navlink
from .theme import ThemeComponent
from .notifications import NotificationsContainer

import dash_mantine_components as dmc
from dash.development.base_component import Component


def create_appshell(content: Component):
    return dmc.MantineProvider(
        forceColorScheme=ThemeComponent.base_colors_scheme,
        theme=ThemeComponent.theme,
        children=dmc.AppShell(
            padding="md",
            header={'height': 52},  
            children=[
                dmc.AppShellMain(content),
                NotificationsContainer(),
                dmc.AppShellHeader(
                    display='flex',
                    style={'alignItems': 'center'},
                    mx='md',
                    children=[
                        dmc.Flex(get_icon("mingcute:flash-circle-line", height=35), mr='auto', align='center', justify='center'),
                        dmc.NavLink(
                            href="/",
                            leftSection=get_icon('material-symbols:home-outline-rounded'),
                            label='Home',
                            w='8rem',
                            active='exact'
                        ),
                        dmc.NavLink(
                            href="/dashboard",
                            leftSection=get_icon('icon-park-outline:sales-report'),
                            label='Dashboard',
                            w='8rem',
                            active='exact'
                        ),
                        dmc.NavLink(
                            href="/ops-tasks",
                            leftSection=get_icon('majesticons:file-line'),
                            label='Ops Tasks',
                            w='8rem',
                            active='exact'
                        ),
                        dmc.Box(
                            ml='auto',
                            children=dmc.Menu([
                                dmc.MenuTarget(
                                    dmc.ActionIcon(
                                        get_icon(
                                            "material-symbols:settings-outline-rounded", height=30
                                        ),
                                        size="xl",
                                        variant="subtle",
                                    )
                                ),
                                dmc.MenuDropdown([dmc.Group(["Theme", ThemeComponent()], m="sm")]),
                            ],
                            trigger="hover",
                            position="bottom",
                        )),
                    ]
                )
            ],  
        ),
    )
