"""Home page definition for the Lexicard application.

This module renders the landing page for authenticated users,
providing links to primary application features and a logout option.
"""

from nicegui import Client, app, ui

from .front_commons import display_message, display_text, frame


@ui.page("/")
async def homepage(client: Client) -> None:
    """Render the application home page."""
    await client.connected()

    def logout() -> None:
        """Clear session storage and redirect to the login page."""
        app.storage.user.clear()
        app.storage.tab.clear()
        ui.navigate.to("/login")

    with frame("Home"):
        username = app.storage.user.get("username", "Guest")
        display_text(f"Hello {username}!").classes("text-2xl")
        display_message("This is the home page.")
        display_text("Use the menu on the top right to navigate.")

        ui.row()
        ui.button("Make or edit a deck", on_click=lambda: ui.navigate.to("/page_deck"))
        ui.button("Choose a deck to practice", on_click=lambda: ui.navigate.to("/page_deck"))

        ui.row()
        ui.button("Logout", on_click=logout, icon="logout").props("outline round")
