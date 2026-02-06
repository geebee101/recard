# Practice mode audio page
from asyncio import sleep
from nicegui import Client, ui
from front_commons import message, frame, get_command_bar, notify, report_typo, text, get_deck, notify_dev


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
            ### DISABLED TO CHECK different toolbars with diff pages/users
            ### ui.button(icon='expand_more').classes('h-8 hover:shadow').tooltip('TODO what was that again?')
            ui.button(icon='bug_report', on_click=lambda: report_typo('aCard')).classes('h-8 hover:shadow').tooltip('Report a typo')
        ui.space()
        with ui.button_group().props('flat').classes('h-8'):
            ui.button(icon='chevron_right').classes('h-8 hover:shadow').tooltip('Next card')

###content = None

@ui.page('/page_mode_audio')
async def mode_audio_page(client: Client) -> None:
    ###global content
    await client.connected()
    deck = get_deck()
    if not deck:
        message('You need to select a deck, redirecting in 2s...')
        async def nodeck_navigate():
            await sleep(2)
            ui.navigate.to('/page_deck')
        await nodeck_navigate()
        return
    with frame('Practice in mode audio') as content:
        message('To be completed')
        text('Use the menu on the top right to navigate.')
        text('This is just a variant of Single with different sets of shown/hidden reveals')
        text('Once implementation overall is more stable, it might be expedient to write as a query variant:')
        text('e.g. .../page_mode_single?m=audio')
        text('Let\'s sort out the Settings first')
        #ui.button('Back', on_click=ui.navigate.back)
        add_cmdbar()

