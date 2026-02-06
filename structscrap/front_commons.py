# front_commons: theme, frame, menu
from typing import Optional
from contextlib import contextmanager
from nicegui import ui, app
from starlette.responses import RedirectResponse
from probbucket import ProbBucket

### UNUSED? button_container = None
# each page can fill the cmd bar w diff buttons
command_bar = None
DEV = True # are we in developper mode?

# TODO once we have the User and the Deck, these should be replaced with bindings
deck_button = None
user_streak = 0
user_best_ever = 0
user_best_in_streak = 0
daily_score = 0
deck = None
bucks = None

# local state / app (session)
class Tally:
    def __init__(self):
        self.tally = 0
daily_score = Tally()

# TODO While there are globals, the app cannot be multi-users!!! seems to work though
# still unclear which variables are shared when using nicegui, NOT transparent

def get_command_bar():
    return command_bar

def get_deck():
    global deck
    try: ### TODO TEMP remove after testing
        deck  = app.storage.tab.get('deck', None)
        if deck:
            notify_dev(f'1st: {deck.cards[0].target_word}', 'positive')
        else:
            notify_dev('No deck?!?', 'negative')
        return deck
    except RuntimeError: # app.storage.tab can only be used with a client connection
        print('### RuntimeError: app.storage.tab can only be used with a client connection')
        notify_dev('NO ACCESS TO STOW YET!', 'warning')
        return None

def get_bucks():
    """
    Obtain the user's probbucket.

    demo: build a pb on the demodeck.
    """
    global bucks
    if bucks: return bucks
    bucks = ProbBucket()
    dk = get_deck()
    if dk: 
        bucks.add_cards(deck.cards)
    return bucks

def add_style(): 
    """for centered-wrapped-text (not in Quasar/Tailwind)
    
    plus an attempt a multi-lines notif DOES NOT WORK
    other styles to be defined by functions using Tailwind
    """
    ui.add_css('''
    .centered-wrapped-text {
        /* Centers all lines of the text block */
        text-align: center;
        /* Ensures long, unbreakable strings break to stay within the container */
        overflow-wrap: break-word; /* Official property name */
        word-wrap: break-word;   /* Legacy alias for broader compatibility */
        /* Optional: Balances line lengths for better aesthetics in headings/short text */
        text-wrap: balance;
    };
    .multi-line-notification { white-space: pre-line; }
    ''')

@ui.page("/login")
def login(redirect_to: str = '/') -> Optional[RedirectResponse]:
    """login page, purposedly not bearing app marks, works in tandem with middleware in auth.py
    
    Middleware intercept any attempt to open a page and navigate here.
    Once logged in the user is redirect to the original page requested.
    """
    passwords = {'toto': 'toto'}
    def try_login() -> None:  # local function to avoid passing username and password as arguments
        if passwords.get(username.value) == username.value:
            app.storage.user.update({'username': username.value, 'authenticated': True})
            ui.navigate.to(redirect_to)  # go back to where the user wanted to go
        else:
            ui.notify('Wrong username or password', color='negative')

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/')
    with ui.column().classes('absolute-center items-center'):
        message('Login with your Atmosphere account')
        ui.label('e.g. ny.tngl.sh or my.bsky.social, etc.').classes('text-grey-8 centered-wrapped-text')
        ui.label('you will be redirected to your server for authentication').classes('text-grey-8 centered-wrapped-text')
        with ui.card():
            username = ui.input('Username').on('keydown.enter', try_login)
            #password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login)
            ui.button('Log in', on_click=try_login)
    return None

@contextmanager
def frame(navigation_title: str, buttons_func = None):
    """Custom page frame to share the same styling and behavior across all pages"""
    global button_container, command_bar
    ui.page_title('pre-Recard')
    if not app.storage.user.get('authenticated'):
        # Use a FastAPI response for redirection
        return RedirectResponse('/login')
    ui.colors(primary='#9bf8b2', secondary='#53B689', accent='#03300e', positive='#53B689')
    add_style()
    with ui.header(elevated=True).classes('items-center h-10 py-0'):
        with ui.button().props(' flat color=grey round size="sm"').classes('p-0'):
            ui.html('&copy;', sanitize=False)
            with ui.tooltip().classes('bg-brown-3 w-40 text-white'):
                ui.html('&copy; 2026 แรช for newthai', sanitize=False)
        ### Too long on mob ui.label('pre-Recard ' + navigation_title).classes('font-bold').classes(replace='text-grey-8')
        ui.space()
        if deck := get_deck():
            ui.label(f'cards: {len(deck.cards)}')
            ui.badge(0, color='skyblue').props('align: middle').bind_text_from(daily_score, 'tally')
        with ui.button(icon='menu').props('flat color=white round'):
            with ui.menu():
                ui.menu_item('Home', on_click=lambda: ui.navigate.to('/'))
                ui.separator() # TEST SECTION 
                with ui.menu_item('TEST SECTION', auto_close=False):
                    with ui.item_section().props('side'):
                        ui.icon('keyboard_arrow_right')
                    with ui.menu().props('anchor="top end" self="top start" auto-close'):
                        ui.menu_item('Ex. page by a function', on_click=lambda: ui.navigate.to('/a'))
                        ui.menu_item('Ex. page by a Class', on_click=lambda: ui.navigate.to('/b'))
                        ui.menu_item('Blank page', on_click=lambda: ui.navigate.to('/page_blank'))
                        ui.menu_item('404', on_click=lambda: ui.navigate.to('/page_non'))
                ui.separator() 
                # submenu
                ui.menu_item('Deck page', on_click=lambda: ui.navigate.to('/page_deck'))
                with ui.menu_item('Practice', auto_close=False):
                    with ui.item_section().props('side'):
                        ui.icon('keyboard_arrow_right')
                    with ui.menu().props('anchor="top end" self="top start" auto-close'):
                        ui.menu_item('Mode single', on_click=lambda: ui.navigate.to('/page_mode_single'))
                        ui.menu_item('Mode audio', on_click=lambda: ui.navigate.to('/page_mode_audio'))
                        ui.menu_item('Mode multi', on_click=lambda: ui.navigate.to('/page_mode_multi'))
                        ui.menu_item('Mode missing', on_click=lambda: ui.navigate.to('/page_mode_missing'))
                ui.separator() 
                ui.menu_item('Profile', on_click=lambda: ui.navigate.to('/page_profile')) # TODO
                ui.separator() 
                ui.menu_item('About', on_click=lambda: ui.navigate.to('/page_about')) # TODO
    with ui.footer(fixed=True).classes('items-center h-10 py-0 gap-0 p-0') as ft:
        # the cmd bar is controlled by each page
        command_bar = ft 
    with ui.scroll_area().classes('w-full h-[calc(100dvh-7rem)] overflow-y-auto  ') as main_content:
        # overflow-y-auto: Adds a vertical scrollbar only if the content overflows vertically.
        # liked it better when small content was also vertically centered, 
        # but doesn't seem compatible with auto scroll
        with ui.column().classes('w-full start items-center justify-center'): # items-center=each ui elements
                yield
        # TODO absolute-center looks much better for sharp short pages, BUT wreak havok if the page requires scrolling :(
    ### print(command_bar)

def message(text):
    """display with formatting for page heading
    """
    label = ui.label(text).classes('text-h4 text-grey-8 centered-wrapped-text')
    return label

def text(text):
    """display with formatting for page text
    """
    label = ui.label(text).classes('text-grey-8 centered-wrapped-text')
    return label

def menu() -> None:
    """Test menu, this will be removed TODO
    """
    ui.link('Home', '/').classes(replace='text-grey-8')
    ui.link('A', '/a').classes(replace='text-grey-8')
    ui.link('B', '/b').classes(replace='text-grey-8')
    ui.link('Blank', '/page_blank').classes(replace='text-grey-8')
    ui.link('404', '/c').classes(replace='text-white') # this will 404!

def notify(text, type = None):
    # type: str 'negative' 'positive' 'warning'
    # no way to offset in nicegui or quasar, will req html/css?
    # the css doesn't look like it is applied to any html element?!?
    ui.notify(text, position='bottom-left', type = type, multi_line=True, classes='multi-line-notification') 

def notify_dev(text, type = None):
    if DEV: notify('DEV-'+text, type = None)

def report_typo(aCard):
    """report a typo, not an app bug, opens a dialog and wait for more info

    - stored by the service (not user, not deck maker)
    can be used to 'deprecate' decks in ranking, 
    and/or reported back to deckmaker if their settings allows feedback
    """
    with ui.context.client.content:
        with ui.dialog() as dialog, ui.card():
            ui.label(f'Typo on {aCard}?').classes('text-h5 text-bold')
            with ui.column().classes('gap-0'):
                typo_spelling = ui.checkbox('Target spelling')
                typo_audio = ui.checkbox('Audio')
                typo_phonetics = ui.checkbox('Phonetics') # TODO if deck capability
                typo_translation = ui.checkbox('Translation')
            with ui.row():
                ui.button('Cancel', on_click=lambda: dialog.submit('Cancel'))
                ui.button('Report', on_click=lambda: dialog.submit('Report'))
        async def show():
            print(dialog)
            result = await dialog
            if result == 'Report':
                notify(f'You reported: \n {typo_spelling.text} \n {typo_audio.text} \n {typo_phonetics.text} \n {typo_translation.text}')
                # TODO another ui thingy that doesn't seem to work as advertised.
                # is it because of the format(), are the newlines lost during format?
                # nope
                pass # to include previous comt when collapsing

    return show() # it works, but I don't understand why

# any other button should prob be handled on their own page?
# we'll see if it leads to too much code repeat.

#.end