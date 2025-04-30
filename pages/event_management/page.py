from utils.helpers import get_icon
from .components.actionbar import EventActionBar
from .components.form import EventFormModal
from .components.table import create_events_table
from .models import EventsQueryParams, EventsModel
from .api import get_events


from flash import register_page
import dash_mantine_components as dmc
from pydantic import ValidationError

register_page(__name__, path='/events', title='Events')

async def layout(**kwargs):

    try:
        filters = EventsQueryParams(**kwargs)

    except ValidationError as e:
        return dmc.Alert(
            color='red',    
            icon=get_icon('material-symbols:error-outline-rounded'),
            title='Validation Error',
            children=str(e)
        )
    
    data = await get_events(filters.db_search_value)
    events = EventsModel.from_db(data)

    content = (
        create_events_table(events) 
        if len(events) > 0 else 
        dmc.Alert(
            icon=get_icon('material-symbols:error-outline-rounded'),
            title='No Data',
            children='Nothing to display'
        )
    )
    
    return_button = dmc.Anchor(
        href='/events',
        children=dmc.Badge(
            leftSection=get_icon('material-symbols:arrow-circle-left-outline-rounded'),
            variant='outline',
            children='Return To Dashboard',
            className='return-button',
        ),
    )

    return dmc.Stack(
        [
            EventActionBar(filters),
            return_button if filters.search_value else None,
            dmc.Center(dmc.Paper(
                content, 
                withBorder=True,
                w=1200,
                p='md',
                mt='md'
            )),
            EventFormModal()
        ]
    )