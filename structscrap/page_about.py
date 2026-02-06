# About page
from nicegui import ui
from front_commons import message, frame, get_command_bar, notify, report_typo, text


content = None

@ui.page('/page_about')
def about_page() -> None:
    global content
    with frame('About this app') as content:
        message('Lexicard a.k.a. pre- recard.social')
        text('Lexicard: An SRS-type app to practice a Thai lexicon')
        text('pre-recard.social: a prototype of an Atmosphere SRS-type')
        text('daily streaks and daily reps of SRS have been banned (see design goals)')
        ui.row()
        text('Use the menu on the top right to navigate.')

        ui.button('Back', on_click=ui.navigate.back)

        with ui.label():
            ui.html('&copy; 2026 แรช for newthai', sanitize=False)
