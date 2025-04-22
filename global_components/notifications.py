from dash import html
import dash_mantine_components as dmc 


class NotificationsContainer(html.Div):
    
    class ids:
        container = 'notifications-container'

    def __init__(self):
        super().__init__(
            children=[
                dmc.NotificationProvider(position='top-right', limit=2),
                html.Div(id=self.ids.container)
            ]
        )