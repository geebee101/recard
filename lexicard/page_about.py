"""About page for the Lexicard application.

This module provides information about the application's purpose, design goals,
and copyright information.
"""

from nicegui import Client, ui

from .front_commons import display_message, display_text, frame


@ui.page("/page_about")
async def about_page(client: Client) -> None:
    """Render the application's 'About' page."""
    await client.connected()
    with frame("About this app"):
        display_message("Lexicard a.k.a. pre-recard.social")

        display_text("Lexicard: An SRS-type app to practice a Thai lexicon")
        display_text("pre-recard.social: A prototype of an Atmosphere SRS-type application.")
        display_text("Note: Daily streaks and repetitive SRS drills have been banned per design goals.")

        ui.row().classes("my-4")
        display_text("Use the menu on the top right to navigate.")

        ui.button("Back", on_click=ui.navigate.back).props("outline").classes("mt-4")

        with ui.label().classes("mt-8"):
            ui.html("&copy; 2026 แรช for newthai", sanitize=False)
