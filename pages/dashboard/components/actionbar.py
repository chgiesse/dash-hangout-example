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


    # Clientside callback to update URL based on filter selections
    update_url_csc = clientside_callback(
        '''
        //js
        function (nClicks, categories, dateRange, ratings, granularity, currentUrl) {
            if (nClicks) {
                // Parse the current URL
                const url = new URL(currentUrl, window.location.origin);
                
                // Set or update query parameters
                if (categories && categories.length > 0) {
                    url.searchParams.set('categories', JSON.stringify(categories));
                } else {
                    url.searchParams.delete('categories');
                }
                
                if (dateRange && dateRange.length === 2) {
                    url.searchParams.set('sale_date_range', JSON.stringify(dateRange));
                } else {
                    url.searchParams.delete('sale_date_range');
                }
                
                if (ratings && ratings.length === 2) {
                    url.searchParams.set('rating_range', JSON.stringify(ratings));
                } else {
                    url.searchParams.delete('rating_range');
                }
                
                if (granularity) {
                    url.searchParams.set('granularity', granularity);
                } else {
                    url.searchParams.delete('granularity');
                }
                
                // Update the browser URL
                window.dash_clientside.set_props('_pages_location', {href: url.toString()});
            }
            return window.dash_clientside.no_update;
        }
        ;//
        ''',
        Output('_pages_location', 'href'),
        Input(ids.filter_button, 'n_clicks'),
        State(ids.category_select, 'value'),
        State(ids.date_picker, 'value'),
        State(ids.rating_slider, 'value'),
        State(ids.granularity_select, 'value'),
        State('_pages_location', 'href'),
        prevent_initial_call=True
    )
    
    # Reset button callback to clear all filters
    reset_url_csc = clientside_callback(
        '''
        //js
        function (nClicks) {
            if (nClicks) { return '' };
            return window.dash_clientside.no_update;
        }
        ;//
        ''',
        Output('_pages_location', 'search', allow_duplicate=True),
        Input(ids.reset_button, 'n_clicks'),
        prevent_initial_call=True
    )

    def __init__(self, filters: AmazonQueryParams):
        print('filters: ', filters, flush=True)
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
            justify='flex-end',
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