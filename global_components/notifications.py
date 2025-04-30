from flash import set_props
from dash import html
import dash_mantine_components as dmc 


class NotificationsContainer(html.Div):
    
    class ids:
        container = 'notifications-container'

    @classmethod
    def send_notification(cls, title: str, message: str, color: str):
        set_props(
            cls.ids.container,
            dmc.Notification(
                title=title,
                message=message,
                color=color,
                action='show'
            )
        )

    def __init__(self):
        super().__init__(
            children=[
                dmc.NotificationProvider(position='top-right', limit=2),
                html.Div(id=self.ids.container)
            ]
        )