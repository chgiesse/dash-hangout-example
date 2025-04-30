from utils.helpers import get_icon
from .form import EventFormModal
from ..models import EventsQueryParams

import dash_mantine_components as dmc 
from flash import clientside_callback, Input, State, Output

class EventActionBar(dmc.Group):

    class ids:
        search_input = 'event-search-input'
        search_button = 'event-search-button'
        add_button = 'add-event-button'

    update_url_csc = clientside_callback(
        '''
        //js
        ( nClicks, searchValue ) => { 
            const setProps = window.dash_clientside.set_props;
            if ( nClicks ) { 
                const qs = '?search_value=' + searchValue 
                setProps('_pages_location', {'search': qs})
            };
        }
        ;//
        ''',
        Input(ids.search_button, 'n_clicks'),
        State(ids.search_input, 'value')
    )

    show_form_csc = clientside_callback(
        '( nClicks ) => { return nClicks ? true : false }',
        Output(EventFormModal.ids.modal, 'opened'),
        Input(ids.add_button, 'n_clicks'),
    )

    def __init__(self, filters: EventsQueryParams):

        super().__init__(
            children=[
                dmc.Title('Event Management', order=2, mr='auto'),
                dmc.Button(
                    leftSection=get_icon('gg:add'),
                    children='Add Event',
                    id=self.ids.add_button,
                    disabled=True if filters.db_search_value else False
                ),
                dmc.TextInput(
                    placeholder='Search Events',
                    id=self.ids.search_input,
                    value=filters.ui_search_value,
                    w=250
                ),
                dmc.ActionIcon(
                    get_icon('material-symbols:search-rounded'),
                    id=self.ids.search_button,
                    size='lg',
                    variant='light',
                ),
            ]
        )