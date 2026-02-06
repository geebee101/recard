# Deck making page
from nicegui import Client, ui, app
from front_commons import message, frame, get_command_bar, notify, report_typo, text, get_deck, notify_dev
from models2 import load_deck_from_json_file, file_path
from models2 import Deck, Lexicard

content = None

@ui.page('/page_deck')
async def deck_page(client: Client) -> None:
    global content
    await client.connected()
    with frame('Deck') as content:
        message('Select a Deck, or create one')

        deck = get_deck()
        if not deck: # simulation of user selecting a deck and loading it
            deck = load_deck_from_json_file(file_path)
            app.storage.tab.update({'deck': deck})
            notify_dev('Now, we have a deck', 'positive')
        text('You have selected:').classes('bg-red-5') ### TODO chaining not working with text color override?!?
        with ui.card().classes('gap-0 p-2'):
            with ui.grid(columns=2):
                ui.input(label='Name', value = deck.name).props('readonly')
                ui.input(label='Author', value = deck.author).props('readonly').classes('mb-0')
                ui.input(label='Language', value = deck.target_language).props('readonly')
                ui.number(label='Cards', value = len(deck.cards)).props('readonly')
                ui.textarea(label='Description', value = deck.description).props('readonly rows=2 w-full').classes('col-span-full')
        ui.row()
        cards = deck.cards
        # Generate columns and rows dynamically
        columns = [{'name': k, 'label': k.capitalize(), 'field': k} for k in Lexicard.model_fields.keys()]
        rows = [card.model_dump() for card in cards[:5]] ### TODO UNSAFE
        table = ui.table(columns=columns, rows=rows, row_key='name', column_defaults={
            'align': 'left h-8',
            'headerClasses': 'uppercase text-white bg-primary h-10',
            }).props('table-header-style="height: 10px"')
        table.columns[0]['classes'] = 'hidden'
        table.columns[0]['headerClasses'] = 'hidden'
        table.columns[2]['classes'] = 'hidden'
        table.columns[2]['headerClasses'] = 'hidden'
        table.update()
