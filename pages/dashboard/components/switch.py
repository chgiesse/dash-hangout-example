import dash_mantine_components as dmc

def create_agg_switch(switch_id: str, checked: bool = False, title: str = 'Relative'):
    return dmc.Switch(
        id=switch_id, 
        size='sm', 
        checked=checked,
        label=title,
        m='sm',
        labelPosition='left',
        styles={'labelWrapper': {'marginRight': 'auto'}},
    )