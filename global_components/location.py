from dash import dcc


class Url(dcc.Location):

    class ids:
        location = 'global-location-component'

    def __init__(self) -> None:
        super().__init__(id=self.ids.location, refresh=False)