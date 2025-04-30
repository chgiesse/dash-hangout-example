from global_components.location import Url
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
        sentiment_select = 'amazon-sentiment-select'
        filter_button = 'amazon-filter-button'
        reset_button = 'amazon-reset-button'


    # Clientside callback to update URL based on filter selections
    update_url_csc = clientside_callback(
        '''
        //js
        function updateUrlParameters(nClicks, categories, dateRange, ratings, granularity, sentiment, currentUrl) {
            // Only proceed if the function was triggered by a click
            if (!nClicks) return window.dash_clientside.no_update;
            
            const url = new URL(currentUrl, window.location.origin);
            const parameterMap = [
                { param: 'categories', value: categories, condition: categories?.length > 0, jsonify: true },
                { param: 'sale_date_range', value: dateRange, condition: dateRange?.length === 2, jsonify: true },
                { param: 'rating_range', value: ratings, condition: ratings?.length === 2, jsonify: true },
                { param: 'sentiment', value: sentiment, condition: sentiment, jsonify: true },
                { param: 'granularity', value: granularity, condition: granularity, jsonify: false }
            ];
            
            parameterMap.forEach(({ param, value, condition, jsonify }) => {
                if (condition) {
                url.searchParams.set(param, jsonify ? JSON.stringify(value) : value);
                } else {
                url.searchParams.delete(param);
                }
            });
            
            window.dash_clientside.set_props('_pages_location', { href: url.toString() });
            }
        ;//
        ''',
        Input(ids.filter_button, 'n_clicks'),
        State(ids.category_select, 'value'),
        State(ids.date_picker, 'value'),
        State(ids.rating_slider, 'value'),
        State(ids.granularity_select, 'value'),
        State(ids.sentiment_select, 'value'),
        State('_pages_location', 'href'),
        prevent_initial_call=True
    )
    
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
            children=dmc.RangeSlider(
                value=filters.rating_range,
                step=.1,
                minRange=minr,
                max=maxr,
                id=self.ids.rating_slider,
            )
        )

        gran_radio_group = dmc.RadioGroup(
            children=dmc.Stack(
                [dmc.Radio(val.title(), value=val) for val in filters.get_granularities()]
            ),
            label='Select Granularity',
            value=filters.granularity,
            id=self.ids.granularity_select,
        )

        sentiment_radio_group = dmc.InputWrapper(
            label='Select Sentiment',
            children=dmc.Group(
                justify="flex-start",
                children=dmc.ChipGroup(
                    [dmc.Chip(val.title(), value=val) for val in filters.get_sentiments()],
                    multiple=True,
                    value=filters.sentiment,
                    id=self.ids.sentiment_select,
                )
            )
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
            gap='lg',
            children=[
                cat_select,
                sale_date_picker,
                rating_slider,
                sentiment_radio_group,
                gran_radio_group,
                buttons
            ],
        )