# blank page
from nicegui import ui
from front_commons import message, frame, get_command_bar, notify, report_typo, text


def add_cmdbar():
    cmds = get_command_bar()
    with cmds:
        # because 'flat' on a button makes it disappear altogether WTF
        with ui.button_group().props('flat').classes('h-8'):
            ui.button(icon='chevron_left', on_click=lambda: notify('Yeah!', type='positive')).classes('h-8 hover:shadow').tooltip('Previous card')
        ui.space()
        # done loop expand_more|unfold_more bug_report stop|back_hand
        with ui.button_group().props('flat').classes('h-8') as bc: #
            ui.button(icon='done').classes('h-8 hover:shadow').tooltip('I know the answer')
            ui.button(icon='loop').classes('h-8 hover:shadow').tooltip('I need the reveal')
            ui.button(icon='expand_more').classes('h-8 hover:shadow').tooltip('TODO what was that again?')
            ui.button(icon='bug_report', on_click=lambda: report_typo('aCard')).classes('h-8 hover:shadow').tooltip('Report a typo')
        ui.space()
        with ui.button_group().props('flat').classes('h-8'):
            ui.button(icon='chevron_right').classes('h-8 hover:shadow').tooltip('Next card')

content = None

@ui.page('/page_blank')
def blank_page() -> None:
    global content
    with frame('Blank') as content:
        message('Page intentionally left blank.')
        text('Use the menu on the top right to navigate.')
        text('TODO: back button in footer? ?? No, we don\'t really need that, now that we have resolved the command bar').classes('centered-wrapped-text')
        ui.button('Back', on_click=ui.navigate.back)
        add_cmdbar()
###        has_typo('aCard') # demo this should be an actual card, not a string

