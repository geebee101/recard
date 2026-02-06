"""A placeholder blank page for the Lexicard application.

This module provides a template for new pages and serves as a navigation placeholder.
"""

from nicegui import Client, ui

from .front_commons import display_message, display_text, frame, get_command_bar, notify, report_typo


def add_placeholder_command_bar() -> None:
    """Add standardized placeholder buttons to the command bar footer."""
    command_bar = get_command_bar()
    if not command_bar:
        return

    with command_bar:
        with ui.button_group().props("flat").classes("h-8"):
            ui.button(
                icon="chevron_left", on_click=lambda: notify("Not implemented", type="warning")
            ).classes("h-8 hover:shadow").tooltip("Previous")

        ui.space()

        with ui.button_group().props("flat").classes("h-8"):
            ui.button(icon="done").classes("h-8 hover:shadow").tooltip("Action 1")
            ui.button(icon="loop").classes("h-8 hover:shadow").tooltip("Action 2")
            ui.button(icon="bug_report", on_click=lambda: report_typo("Placeholder Card")).classes(
                "h-8 hover:shadow"
            ).tooltip("Report Typo")

        ui.space()

        with ui.button_group().props("flat").classes("h-8"):
            ui.button(icon="chevron_right").classes("h-8 hover:shadow").tooltip("Next")


@ui.page("/page_blank")
async def blank_page(client: Client) -> None:
    """Render the blank placeholder page."""
    await client.connected()
    with frame("Blank"):
        display_message("Page intentionally left blank.")
        display_text("Use the menu on the top right to navigate.")
        display_text("This page serves as a future feature placeholder.")

        ui.button("Back", on_click=ui.navigate.back).props("outline").classes("mt-4")
        add_placeholder_command_bar()
