"""User profile page for settings and learning statistics.

This module renders the user's profile details, including signup information,
all-time high scores, and current learning streak.
"""

from nicegui import Client, app, ui

from .front_commons import display_message, display_text, frame
from .models import TOTO_DATA, User


@ui.page("/page_profile")
async def profile_page(client: Client) -> None:
    """Render the user profile page."""
    await client.connected()

    # DEV TODO: Replace with actual database user retrieval
    current_user = User.model_validate(TOTO_DATA)

    with frame("Profile"):
        display_message("User Profile")
        ui.row()

        username = app.storage.user.get("username", "Unnamed")
        display_text(f"Username: {username} (ID: {current_user.tid})")
        display_text(f"Member since: {current_user.signup_tstamp.strftime('%Y-%m-%d')}")

        ui.row()
        display_text(f"Current Streak: {current_user.streak} days")
        display_text(f"All-time High Score: {current_user.highest_score_ever}")
        display_text(f"30-day High Score: {current_user.highest_score_30d}")

        ui.separator().classes("my-4")

        with ui.grid().classes("grid-cols-2 gap-2 w-full max-w-md"):
            for field, value in current_user.model_dump().items():
                ui.label(f"{field.replace('_', ' ').capitalize()}:").classes("font-bold text-right pr-2")
                ui.label(str(value))

        ui.row().classes("mt-4")
        ui.button("Back", on_click=ui.navigate.back).props("outline")
