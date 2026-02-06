# Practice mode multi page
from random import shuffle
from asyncio import sleep
from nicegui import Client, ui
from front_commons import message, frame, get_command_bar, notify, report_typo, text, get_deck, notify_dev, get_bucks, daily_score
from main import auto_play


# local state
class Question:
    def __init__(self):
        self._card = None
        # ui elements
        self.chips = []
    def set_cards(self, card_list): # list of 3 cards
        """
        Sets the question card, as well as 2 wrong answers.
        """
        card = card_list[0] # the question
        self._card = card
        # could make binding work unless direct props
        self.target_word = card.target_word
        self.sound = card.sound
        self.phonetic = card.phonetic
        self.explain = card.explain
        self.choices, self.value = build_choices(card_list)
        # also need direct vars for binding
        self.choice0 = self.choices[0]
        self.choice1 = self.choices[1]
        self.choice2 = self.choices[2]

question = Question()

def add_cmdbar():
    cmds = get_command_bar()
    with cmds:
        # because 'flat' on a button makes it disappear altogether WTF
        with ui.button_group().props('flat').classes('h-8'):
            ui.button(icon='chevron_left', on_click=lambda: notify_dev('Yeah!', type='positive')).classes('h-8 hover:shadow').tooltip('Previous card')
        ui.space()
        # done loop expand_more|unfold_more bug_report stop|back_hand
        with ui.button_group().props('flat').classes('h-8') as bc:
            ui.button(icon='loop', on_click=reveal).classes('h-8 hover:shadow').tooltip('I need the reveal')
            #ui.button(icon='expand_more').classes('h-8 hover:shadow').tooltip('TODO what was that again?')
            ui.button(icon='bug_report', on_click=lambda: report_typo('aCard')).classes('h-8 hover:shadow').tooltip('Report a typo')
        ui.space()
        with ui.button_group().props('flat').classes('h-8'):
            ui.button(icon='chevron_right').classes('h-8 hover:shadow').tooltip('Next card')

def build_choices(card_list):
    choices = [c.explain for c in card_list]
    shuffle(choices)
    value = choices.index(question.explain)
    return choices, value

def pick_next():
    cards = get_bucks().pick_3_cards()
    question.set_cards(cards)
    for chip in question.chips:
        chip.set_enabled(True)
        chip.selected = False
        chip.classes(remove='text-bold').props(remove='outline color=red').props('color=primary')
        print('Removed?')

### CAUTION button on_click= func, as onclick=func() will execute it immediately
def reveal():
    for c in [0, 1, 2]:
        chip = question.chips[c]
        chip.set_enabled(False)
        if c == question.value:
            chip.classes('text-bold')
            chip.props('color=primary')
            if chip.selected:
                score(1)
        else: # incorrect answer
            if chip.selected:
                chip.props('color=red')
                score(-1)
            else:
                chip.props('outline color=red')
    ui.timer(2, pick_next, once=True)

def score(n: int):
    """
    Record score if positive, and move on to next card. Refreshes cmd bar to default if required.
    """
    bk = get_bucks()
    if n == 1:
        daily_score.tally += 1
        bk.promote(question._card, True)
    else:
        bk.demote(question._card)
    notify_dev(f'button w.{n} score={daily_score.tally}')

def user_has_chosen(e):
    if e.sender.selected == True:
        notify_dev('We have a winner!')
        ui.timer(2, reveal, once=True)

@ui.page('/page_mode_multi')
async def mode_multi_page(client: Client) -> None:
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
    pick_next()
    with frame('Practice in mode multi-choice') as content:
        ui.row()
        message(question.target_word).bind_text_from(question, 'target_word')
        if True: # and ... settings
            text(question.phonetic).bind_text_from(question, 'phonetic')
        sd = question.sound # TODO audio not refreshed (no binding, not change)
        if sd != '0': # and... settings
            auto_play(sd)
            ui.button(icon='play_arrow', on_click=lambda: auto_play(sd)).classes('h-8 hover:shadow').tooltip('Play audio')
        ui.row()
        text('Select the correct answer:')
        c0 = ui.chip(question.choices[0], selectable=True, on_selection_change=user_has_chosen).bind_text_from(question, 'choice0')
        c1 = ui.chip(question.choices[1], selectable=True, on_selection_change=user_has_chosen).bind_text_from(question, 'choice1')
        c2 = ui.chip(question.choices[2], selectable=True, on_selection_change=user_has_chosen).bind_text_from(question, 'choice2')
        question.chips = [c0, c1, c2]
        # lambda is necessary to prevent immediate execution iff args
        # otherwise pass func, not func()
        ###ui.button('Reveal', on_click=reveal) use bottom button from now on
        add_cmdbar()

