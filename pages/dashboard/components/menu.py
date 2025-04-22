from utils.helpers import get_icon

from dash import dcc
from flash import callback, Input, Output, State, no_update
import dash_mantine_components as dmc 
from datetime import date
from plotly.graph_objects import Figure
import plotly.io as pio
import io


class GraphDownload(dcc.Download):

    class ids:
        download = 'cr-graph-download'

    def __init__(self) -> None:
        super().__init__(
            id=self.ids.download
        )


class GraphMenu(dmc.Menu):

    class ids:
        dl_button = lambda idx: {'type': 'cr-dl-graph-button', 'index': idx}

    @classmethod
    def download_callback(cls, graph_id: str):
        @callback(
            Output(GraphDownload.ids.download, 'data', allow_duplicate=True),
            Input(cls.ids.dl_button(graph_id), 'n_clicks'),
            State(graph_id, 'figure'),
            prevent_initial_call=True
        )
        async def download_graph(_, figure_dict: dict):
            # Convert the plain dictionary to a Plotly Figure object
            try:
                figure = Figure(figure_dict)
            except Exception as e:
                print("Error creating Figure from dict:", str(e), flush=True)
                return no_update

            buffer = io.BytesIO()

            try:
                # Export the Plotly figure to a static image (e.g., PNG)
                pio.write_image(figure, buffer, format='png', scale=5, engine='kaleido')
            except Exception as e:
                print("Error writing image:", str(e), flush=True)
                return no_update

            # Rewind the buffer to the beginning
            buffer.seek(0)

            # Check buffer content size for debugging
            print("Buffer size:", len(buffer.getvalue()), flush=True)

            # Create the file name
            file_name = f"{graph_id}_{date.today()}.png"

            # Return the file as bytes
            return dcc.send_bytes(buffer.read(), filename=file_name)

    
    def __init__(self, graph_id: str, aggregation_items: list = [], application_items: list = []):
        super().__init__(
            position='left-start',
            trigger='hover',
            radius='md',
            children=[
                dmc.MenuTarget(
                    dmc.ActionIcon(
                        children=get_icon('charm:menu-kebab'), 
                        variant='transparent',
                    ),
                ),
                dmc.MenuDropdown(
                    children=[
                        dmc.MenuLabel('Aggregations') if aggregation_items else None,
                        *aggregation_items,
                        dmc.MenuLabel('Application'),
                        *application_items,
                        dmc.MenuItem(
                            'Download',
                            rightSection=get_icon('material-symbols:download-rounded'),
                            id=self.ids.dl_button(graph_id),
                            py='sm',
                            miw=140,
                        )
                    ]
                )
            ]
        )