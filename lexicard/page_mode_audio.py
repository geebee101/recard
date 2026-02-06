"""Practice mode: Audio-only.

This module provides a practice interface where the user primarily listens
to the word before revealing structural details.
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


def add_command_bar_buttons() -> None:
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
            ui.button(icon="loop").classes("h-8 hover:shadow").tooltip("Reveal details")
            ui.button(icon="bug_report", on_click=lambda: report_typo("Draft Card")).classes(
                "h-8 hover:shadow"
            ).tooltip("Report a typo")

        ui.space()

        with ui.button_group().props("flat").classes("h-8"):
            ui.button(icon="chevron_right").classes("h-8 hover:shadow").tooltip("Next card")


@ui.page("/page_mode_audio")
async def mode_audio_page(client: Client) -> None:
    """Render the audio-only practice page."""
    await client.connected()

    deck = get_deck()
    if not deck:
        display_message("No deck selected. Redirecting to deck selection...")
        await asyncio.sleep(2)
        ui.navigate.to("/page_deck")
        return

    with frame("Practice: Audio Mode"):
        display_message("Audio Mode")
        display_text("Listen to the word and try to recall its meaning.")
        display_text("Implementation note: This will be a specialized view of the Single mode.")

        add_command_bar_buttons()
