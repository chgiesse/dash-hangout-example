import dash_mantine_components as dmc
from flash import register_page

register_page(
    __name__, 
    path_template='/events/<event_id>'
)


async def layout(event_id, **kwargs):
    return dmc.Title('Event ID ' + str(event_id))