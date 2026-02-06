"""Practice mode: Multi-choice card selection.

This module provides a practice interface where the user is presented with
one target word and three choices for its translation.
"""

import asyncio
import random
from typing import Any, Optional

from nicegui import Client, ui

from .front_commons import (
    auto_play,
    daily_score,
    display_message,
    display_text,
    frame,
    get_command_bar,
    get_deck,
    get_learning_buckets,
    notify,
    notify_dev,
    report_typo,
)
from .models import Lexicard


class MultiChoiceState:
    """Internal state to track the active question and choices for multi-choice mode."""

    def __init__(self) -> None:
        """Initialize the multi-choice state."""
        self.current_card: Lexicard | None = None
        self.target_word: str = ""
        self.sound: str = "0"
        self.phonetic: str = ""
        self.explain: str = ""
        self.choices: list[str] = ["", "", ""]
        self.correct_index: int = -1
        self.chips: list[ui.chip] = []
        # Bindable choice shortcuts
        self.choice_0: str = ""
        self.choice_1: str = ""
        self.choice_2: str = ""

    def set_cards(self, cards: list[Lexicard]) -> None:
        """Set the current card and build distractors from the provided list.

        Args:
                cards: A list of 3 Lexicard objects (index 0 is the question).
        """
        card = cards[0]
        self.current_card = card
        self.target_word = card.target_word
        self.sound = card.sound
        self.phonetic = card.phonetic
        self.explain = card.explain

        # Build and shuffle choices
        choice_texts = [c.explain for c in cards]
        random.shuffle(choice_texts)

        self.choices = choice_texts
        self.correct_index = choice_texts.index(card.explain)

        # Update shortcuts for binding
        self.choice_0 = choice_texts[0]
        self.choice_1 = choice_texts[1]
        self.choice_2 = choice_texts[2]


# Global state for multi-choice page
state = MultiChoiceState()


def add_multi_choice_command_bar() -> None:
    """Add multi-choice specific buttons to the footer."""
    command_bar = get_command_bar()
    if not command_bar:
        return

    with command_bar:
        with ui.button_group().props("flat").classes("h-8"):
            ui.button(
                icon="chevron_left", on_click=lambda: notify_dev("Previous not implemented", "warning")
            ).classes("h-8 hover:shadow").tooltip("Previous card")

        ui.space()

        with ui.button_group().props("flat").classes("h-8"):
            ui.button(icon="loop", on_click=reveal_answers).classes("h-8 hover:shadow").tooltip(
                "Reveal correct answer"
            )
            ui.button(icon="bug_report", on_click=lambda: report_typo(state.current_card)).classes(
                "h-8 hover:shadow"
            ).tooltip("Report a typo")

        ui.space()

        with ui.button_group().props("flat").classes("h-8"):
            ui.button(icon="chevron_right", on_click=pick_next_question).classes("h-8 hover:shadow").tooltip(
                "Next card"
            )


def reveal_answers() -> None:
    """Reveal the correct answer and mark user selection as right or wrong."""
    for i in range(3):
        chip = state.chips[i]
        chip.set_enabled(False)

        if i == state.correct_index:
            chip.classes("text-bold")
            chip.props("color=primary")
            if chip.selected:
                record_multi_score(1)
        else:
            if chip.selected:
                chip.props("color=red")
                record_multi_score(-1)
            else:
                chip.props("outline color=red")

    ui.timer(2, pick_next_question, once=True)


def pick_next_question() -> None:
    """Select a new set of cards and reset the multi-choice UI."""
    buckets = get_learning_buckets()
    if not buckets:
        return

    cards = buckets.pick_3_cards()
    if all(cards):
        state.set_cards(cards)
        for chip in state.chips:
            chip.set_enabled(True)
            chip.selected = False
            chip.classes(remove="text-bold")
            chip.props(remove="outline color=red").props("color=primary")


def record_multi_score(points: int) -> None:
    """Update learning progress based on correct or incorrect multi-choice selection.

    Args:
            points: 1 for correct, -1 for incorrect.
    """
    buckets = get_learning_buckets()
    if not buckets or not state.current_card:
        return

    if points == 1:
        daily_score.tally += 1
        buckets.promote(state.current_card, high_priority=True)
    else:
        buckets.demote(state.current_card)

    notify_dev(f"Score: {daily_score.tally}")


def on_user_choice(event_args: Any) -> None:
    """Handle user clicking a chip selection."""
    if event_args.sender.selected:
        notify_dev("Choice selected, revealing...")
        ui.timer(1.5, reveal_answers, once=True)


@ui.page("/page_mode_multi")
async def mode_multi_page(client: Client) -> None:
    """Render the multi-choice practice interface."""
    await client.connected()

    deck = get_deck()
    if not deck:
        display_message("Redirecting to deck selection...")
        await asyncio.sleep(2)
        ui.navigate.to("/page_deck")
        return

    # Initial setup
    buckets = get_learning_buckets()
    if buckets:
        initial_cards = buckets.pick_3_cards()
        if all(initial_cards):
            state.set_cards(initial_cards)

    with frame("Practice: Multi-Choice"):
        ui.row().classes("my-4")
        ui.label(state.target_word).classes("text-h2").bind_text_from(state, "target_word")
        ui.label(state.phonetic).classes("text-h5 italic").bind_text_from(state, "phonetic")

        if state.sound != "0":
            auto_play(state.sound)
            ui.button(icon="volume_up", on_click=lambda: auto_play(state.sound)).props("flat round").tooltip(
                "Play audio"
            )

        ui.row().classes("mt-4 items-center")
        display_text("Select the correct translation:")

        with ui.row().classes("gap-4 mt-2"):
            chip0 = ui.chip(
                state.choices[0], selectable=True, on_selection_change=on_user_choice
            ).bind_text_from(state, "choice_0")
            chip1 = ui.chip(
                state.choices[1], selectable=True, on_selection_change=on_user_choice
            ).bind_text_from(state, "choice_1")
            chip2 = ui.chip(
                state.choices[2], selectable=True, on_selection_change=on_user_choice
            ).bind_text_from(state, "choice_2")

        state.chips = [chip0, chip1, chip2]
        add_multi_choice_command_bar()
