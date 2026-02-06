"""Practice mode: Missing word in context.

This module provides a practice interface where the user identifies a word
missing from a sentence or context. (Draft implementation)
"""

import asyncio

from nicegui import Client, ui

from .front_commons import (
    display_message,
    display_text,
    frame,
    get_command_bar,
    get_deck,
    notify,
    report_typo,
)


def add_missing_command_bar() -> None:
    """Add context-specific navigation and action buttons to the footer."""
    command_bar = get_command_bar()
    if not command_bar:
        return

    with command_bar:
        with ui.button_group().props("flat").classes("h-8"):
            ui.button(
                icon="chevron_left", on_click=lambda: notify("Not implemented", type="warning")
            ).classes("h-8 hover:shadow").tooltip("Previous card")

        ui.space()

        with ui.button_group().props("flat").classes("h-8"):
            ui.button(icon="done").classes("h-8 hover:shadow").tooltip("I know the answer")
            ui.button(icon="loop").classes("h-8 hover:shadow").tooltip("Reveal missing word")
            ui.button(icon="bug_report", on_click=lambda: report_typo("Draft Card")).classes(
                "h-8 hover:shadow"
            ).tooltip("Report a typo")

        ui.space()

        with ui.button_group().props("flat").classes("h-8"):
            ui.button(icon="chevron_right").classes("h-8 hover:shadow").tooltip("Next card")


@ui.page("/page_mode_missing")
async def mode_missing_page(client: Client) -> None:
    """Render the missing-word practice page."""
    await client.connected()

    deck = get_deck()
    if not deck:
        display_message("No deck selected. Redirecting...")
        await asyncio.sleep(2)
        ui.navigate.to("/page_deck")
        return

    with frame("Practice: Missing Mode"):
        display_message("Missing Mode")
        display_text("Identify the target word in a sentence context.")
        display_text("Note: This mode is currently under implementation.")

        ui.button("Back", on_click=ui.navigate.back).props("outline").classes("mt-4")
        add_missing_command_bar()
