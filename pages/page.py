from flash import register_page
import dash_mantine_components as dmc 

register_page(__name__, path='/')

async def layout(**kwargs):
    return dmc.Title('HOME')