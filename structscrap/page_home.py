# home page
from front_commons import message, frame, text

from nicegui import ui, app


@ui.page('/')
def homepage() -> None:
###    buttons(None)

    def logout() -> None:
        app.storage.user.clear()
        app.storage.tab.clear()
        ui.navigate.to('/login')

    with frame('Home'):
        text(f'Hello {app.storage.user["username"]}!').classes('text-2xl')
        message('This is the home page.')
        text('Use the menu on the top right to navigate.')
        ui.row()
        ui.button('Make or edit a deck')
        ui.button('Choose a deck to practice')
        ui.row()
        ui.button(on_click=logout, icon='logout').props('outline round')