from global_components.notifications import NotificationsContainer
from ..api import add_event
from ..models import EventFormModel

import dash_mantine_components as dmc
from flash import callback, Input, State, set_props
from pydantic import ValidationError
from datetime import date

class EventFormModal(dmc.Modal):

    class ids:
        name_field = 'events-event-form-name'
        location_field = 'events-event-form-location'
        date_field = 'events-event-form-date'
        button = 'events-event-form-button'
        modal = 'events-form-modal'

    @callback(
        Input(ids.button, 'n_clicks'),
        State(ids.name_field, 'value'),
        State(ids.location_field, 'value'),
        State(ids.date_field, 'value'),
        prevent_initial_call=True
    )

    async def add_event(_, name, location, date):
        try:
            form_data = EventFormModel(
                name=name, location=location, date=date
            )
        
        except ValidationError as e:
            NotificationsContainer.send_notification(
                title='Validation Error',
                message=str(e),
                color='red'
            )
            return

        result = await add_event(form=form_data)
        if isinstance(result, Exception):
            NotificationsContainer.send_notification(
                title='Adding event failed',
                message=str(e),
                color='red'
            )
        
        set_props('_pages_location', {'pathname': '/events'})

    def __init__(self):
        super().__init__(
            opened=False,
            id=self.ids.modal,
            title='Add new event',
            children=dmc.Stack([
                dmc.TextInput(
                    id=self.ids.name_field,
                    value='',
                    label='Enter Event Name'
                ),
                dmc.TextInput(
                    id=self.ids.location_field,
                    value='',
                    label='Enter Location'
                ),
                dmc.DatePickerInput(
                    id=self.ids.date_field,
                    minDate=date.today(),
                    label='Select Event Date'
                ),
                dmc.Button(
                    id=self.ids.button,
                    fullWidth=True,
                    children='Add event'
                )
            ])
        )