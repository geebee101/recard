"""Deck management page for creating and reviewing flashcard decks.

This module provides a UI to load decks from storage, display metadata,
and view card lists in a tabular format.
"""

from nicegui import Client, app, ui

from .front_commons import display_message, display_text, frame, get_deck, notify_dev
from .models import FILE_PATH, Lexicard, load_deck_from_json_file


@ui.page("/page_deck")
async def deck_page(client: Client) -> None:
    """Render the deck overview and selection page."""
    await client.connected()

    with frame("Deck"):
        display_message("Select a Deck, or create one")

        deck = get_deck()
        if not deck:
            # Mock behavior: automatically load the default deck if none selected
            deck = load_deck_from_json_file(FILE_PATH)
            app.storage.tab.update({"deck": deck})
            notify_dev("Default deck loaded from storage", "positive")

        display_text("Currently Selected:").classes("font-bold")

        with ui.card().classes("gap-0 p-2 w-full max-w-2xl"):
            with ui.grid(columns=2).classes("w-full"):
                ui.input(label="Name", value=deck.name).props("readonly")
                ui.input(label="Author", value=deck.author).props("readonly")
                ui.input(label="Language", value=deck.target_language).props("readonly")
                ui.number(label="Cards", value=len(deck.cards)).props("readonly")
                ui.textarea(label="Description", value=deck.description).props("readonly rows=2").classes(
                    "col-span-full"
                )

        ui.row().classes("my-4")

        # Card Data Table
        columns = [
            {"name": k, "label": k.replace("_", " ").capitalize(), "field": k}
            for k in Lexicard.model_fields.keys()
        ]
        # Show first 10 cards as a preview
        rows = [card.model_dump() for card in deck.cards[:10]]

        table = ui.table(
            columns=columns,
            rows=rows,
            row_key="tid",
            column_defaults={
                "align": "left",
                "headerClasses": "uppercase text-white bg-primary",
            },
        ).classes("w-full")

        # Hide specific technical columns
        hidden_cols = {"tid", "check_for_correction"}
        for col in table.columns:
            if col["name"] in hidden_cols:
                col["classes"] = "hidden"
                col["headerClasses"] = "hidden"

        table.update()

        ui.button("Back", on_click=ui.navigate.back).props("outline").classes("mt-4")
