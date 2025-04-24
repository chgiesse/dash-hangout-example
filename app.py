from global_components.appshell import create_appshell
from global_components.theme import ThemeComponent, apply_vizro_theme
from api.setup import setup_db
from flash import Flash, html, page_container, State

import dash_mantine_components as dmc 


app = Flash(
    __name__, 
    suppress_callback_exceptions=True, 
    use_pages=True,
    external_stylesheets=[dmc.styles.DATES],
    routing_callback_inputs={
        'theme': State(ThemeComponent.ids.toggle, 'checked'),
    }
)

apply_vizro_theme()

app.layout = create_appshell(page_container)

app.server.before_serving(setup_db)

if __name__ == '__main__':
    app.run(debug=False)