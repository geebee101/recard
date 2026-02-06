# Profile page : settings, stats
from nicegui import ui, app
from front_commons import message, frame, get_command_bar, notify, report_typo, text
from front_commons import user_streak, user_best_ever, user_best_in_streak
from models2 import toto_user # DEV TODO

content = None

@ui.page('/page_profile')
def profile_page() -> None:
    global content
    with frame('Profile') as content:
        message('Page intentionally left blank.')
        text('Use the menu on the top right to navigate.')
        ui.row()

        name = app.storage.user.get('username', 'unnamed')
        text(f"User Username: {name} tid {toto_user.tid}")
        text(f"Since {toto_user.signup_tstamp}")

        ui.row()
        text(f"Streak (days in last thirty days {toto_user.streak}")
        text(f"Highest ever daily score {toto_user.highest_score_ever}")
        text(f"Highest in last 30 days {toto_user.highest_score_30d}")

        with ui.grid().classes('grid-cols-2 gap-2'):
            for label, value in toto_user.__dict__.items():
                ui.label(f'{label}:').classes('font-bold text-right bg-grey-2') # Align label right
                ui.label(str(value))
        ui.row()
        ui.button('Back', on_click=ui.navigate.back)

""" pydantic model built from:
toto_user = {
    'tid': 1234567890,
    'name': 'toto_user',
    'signup_tstamp': datetime.now(),
    'highest_score_ever': 302,
    'highest_score_30d':101,
    'streak': 21
    }
    """