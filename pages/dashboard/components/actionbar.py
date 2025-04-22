from ..models import AmazonQueryParams
from utils.helpers import get_icon

import dash_mantine_components as dmc 
from flash import clientside_callback, Input, Output, State


class ActionBar(dmc.Stack):

    class ids:
        category_select = 'amazon-category-select'
        date_picker = 'amazon-date-picker'
        rating_slider = 'amazon-rating-slider'
        granularity_select = 'amazon-granularity-select'
        filter_button = 'amazon-filter-button'
        reset_button = 'amazon-reset-button'

    update_url_csc = clientside_callback(
        f'''
        ( filter, select, categories, dateRange, ratings, granularity ) => {{
            console.log(filter, select, categories, dateRange, ratings, granularity)
            const ctx = window.dash_clientside.callback_context
            const triggeredId = ctx.triggered_id

            if ( triggeredId === '{ids.filter_button}') {{
                
            }} else {{
                
            }}
        }}
        ''',
        Input(ids.filter_button, 'n_clicks'),
        Input(ids.reset_button, 'n_clicks'),
        State(ids.category_select, 'value'),
        State(ids.date_picker, 'value'),
        State(ids.rating_slider, 'value'),
        State(ids.granularity_select, 'value'),
    )

    def __init__(self, filters: AmazonQueryParams):
        
        cat_select = dmc.MultiSelect(
            data=[{'value': val, 'label': val.title()} for val in filters.get_categroies()],
            value=filters.categories,
            label='Select Category',
            id=self.ids.category_select
        )

        sale_date_picker = dmc.DatePickerInput(
            value=filters.sale_date_range,
            type='range',
            label='Select Sale Date Range',
            id=self.ids.date_picker,
            numberOfColumns=2,
            dropdownType="modal",
        )

        minr, maxr = filters.get_rating_range()
        rating_slider = dmc.InputWrapper(
            label='Select Rating Range',
            children=dmc.Slider(
                value=filters.rating_range,
                marks=[{'value': val, 'label': str(val)} for val in range(int(minr) + 1, int(maxr) + 1)],
                miw=200,
                min=minr,
                max=maxr,
                id=self.ids.rating_slider,
            )
        )

        gran_radio_group = dmc.RadioGroup(
            children=dmc.Stack([dmc.Radio(val.title(), value=val) for val in filters.get_granularities()]),
            label='Select Granularity',
            value=filters.granularity,
            id=self.ids.granularity_select,
        )
        
        buttons = dmc.Group(
            grow=True,
            children=[
                dmc.Button(
                    'Reset', 
                    id=self.ids.reset_button, 
                    leftSection=get_icon('material-symbols:device-reset-rounded'), 
                    color='red',
                    variant='outline',
                    display='none' if filters.is_default else 'block',
                ),
                dmc.Button(
                    'Filter', 
                    id=self.ids.filter_button, 
                    leftSection=get_icon('material-symbols:filter-alt'),
                    variant='light'
                ),
            ]
        )

        super().__init__(
            m='md',
            children=[
                cat_select,
                sale_date_picker,
                rating_slider,
                gran_radio_group,
                buttons
            ],
        )