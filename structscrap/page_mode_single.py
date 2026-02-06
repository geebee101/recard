# Practice mode single page
from asyncio import sleep # wait for client connection
from nicegui import Client, ui
from starlette.responses import RedirectResponse
from front_commons import message, frame, get_command_bar, notify, report_typo, text, get_deck, notify_dev, get_bucks, daily_score
from main import auto_play

answer = None
reveal_button = None

# local state
class Question:
    def __init__(self):
        self._card = None
    def set_card(self, card):
        self._card = card
        # could make binding work unless direct props
        self.target_word = card.target_word
        self.sound = card.sound
        self.phonetic = card.phonetic
        self.explain = card.explain

question = Question()

def add_cmdbar():
    global reveal_button
    cmds = get_command_bar()
    with cmds:
        # because 'flat' on a button makes it disappear altogether WTF
        with ui.button_group().props('flat').classes('h-8'):
            ui.button(icon='chevron_left', on_click=lambda: score(0)).classes('h-8 hover:shadow').tooltip('Previous card')
        ui.space()
        # done loop expand_more|unfold_more bug_report stop|back_hand
        with ui.button_group().props('flat').classes('h-8') as bc: #
            ui.button(icon='done', on_click=lambda: score(2)).classes('h-8 hover:shadow').tooltip('I know the answer')
            reveal_button = ui.button(icon='loop', on_click=lambda: reveal()).classes('h-8 hover:shadow').tooltip('I need the reveal')
            ui.button(icon='close', on_click=lambda: score(-1)).classes('h-8 hover:shadow').tooltip('TODO what was that again?')
            ui.button(icon='bug_report', on_click=lambda: report_typo('aCard')).classes('h-8 hover:shadow').tooltip('Report a typo')
            ### has_typo('aCard') # demo this should be an actual card, not a string
        ui.space()
        with ui.button_group().props('flat').classes('h-8'):
            ui.button(icon='chevron_right', on_click=lambda: score(0)).classes('h-8 hover:shadow').tooltip('Next card')

def reveal():
    answer.visible = True
    #answer.update()
    reveal_button.disable()
    #reveal_button.update()

def pick_next():
    """
    Pick another card.

    after answer or from next and previous.
    refreshes cmd bar to default.
    """
    question.set_card(get_bucks().pick_card())
    reveal_button.enable()
    answer.visible = False
    return question._card

def score(n: int):
    """
    Record score if positive, and move on to next card. Refreshes cmd bar to default if required.
    """
    bk = get_bucks()
    if n == 2: # card not revealed, high_score
        if reveal_button.enabled:
            daily_score.tally += 2
            bk.promote(question._card, True)
            pick_next()
        else:
            daily_score.tally += 1
            bk.promote(question._card)
            pick_next()
    elif n == 0: # card passed without answer either way
        pass
    elif n == -1: # card failed
        bk.demote(question._card)
        # if not already, reveal and show a while before moving on 
        if not answer.visible:
            reveal() 
            # Schedule the delayed action as a background task
            ui.timer(5, pick_next, once=True) 
        else:
            pick_next()
    notify_dev(f'button w.{n} score={daily_score.tally}')

@ui.page('/page_mode_single')
async def mode_single_page(client: Client) -> None:
    global answer
    await client.connected()
    deck = get_deck()
    if not deck:
        message('You need to select a deck, redirecting in 2s...')
        async def nodeck_navigate():
            await sleep(2)
            ui.navigate.to('/page_deck')
        await nodeck_navigate()
        return
    # first card
    card = get_bucks().pick_card()
    question.set_card(card)
    with frame('Practice in mode single') as content:
        text('What does this mean?')
        # text(deck.name) ### TODO build prob bucket on deck
        add_cmdbar()
        message(card.target_word).bind_text_from(question, 'target_word')
        if True: # and ... settings
            text(card.phonetic).bind_text_from(question, 'phonetic')
        sd = question.sound # TODO audio not refreshed (no binding, not change)
        if sd != '0': # and... settings
            auto_play(sd)
            ui.button(icon='play_arrow', on_click=lambda: auto_play(sd)).classes('h-8 hover:shadow').tooltip('Play audio')
        ui.row()
        answer = text(card.explain)
        answer.bind_text_from(question, 'explain')
        answer.visible = False

"""
    has_sound: str # 0 or fname no ext
    check_for_correction: bool
    phonetic: str
    target_word: str
    explain: str
    """
