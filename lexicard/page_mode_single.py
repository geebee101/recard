"""Practice mode: Single card.

This is the primary study mode where users are presented with one card at a time,
can listen to audio, and reveal the translation and details.
"""

import asyncio
from typing import Optional

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


class QuestionState:
    """Internal state to track the active question card and its observable properties."""

    def __init__(self) -> None:
        """Initialize the question state with empty values."""
        self.current_card: Lexicard | None = None
        self.target_word: str = ""
        self.sound: str = "0"
        self.phonetic: str = ""
        self.explain: str = ""

    def set_card(self, card: Lexicard) -> None:
        """Update the current state from a Lexicard object.

        Args:
                card: The Lexicard instance to load into the view state.
        """
        self.current_card = card
        self.target_word = card.target_word
        self.sound = card.sound
        self.phonetic = card.phonetic
        self.explain = card.explain


# Global module-level state for the page
question_state = QuestionState()
answer_label: ui.label | None = None
reveal_button: ui.button | None = None


def add_practice_command_bar() -> None:
    """Add specialized practice buttons to the application footer."""
    global reveal_button
    command_bar = get_command_bar()
    if not command_bar:
        return

    with command_bar:
        with ui.button_group().props("flat").classes("h-8"):
            ui.button(icon="chevron_left", on_click=lambda: record_score(0)).classes(
                "h-8 hover:shadow"
            ).tooltip("Previous card")

        ui.space()

        with ui.button_group().props("flat").classes("h-8"):
            ui.button(icon="done", on_click=lambda: record_score(2)).classes("h-8 hover:shadow").tooltip(
                "I know the answer"
            )
            reveal_button = (
                ui.button(icon="loop", on_click=reveal_answer)
                .classes("h-8 hover:shadow")
                .tooltip("Reveal translation")
                .mark("Reveal Answer")
            )
            ui.button(icon="close", on_click=lambda: record_score(-1)).classes("h-8 hover:shadow").tooltip(
                "I don't know it"
            )
            ui.button(icon="bug_report", on_click=lambda: report_typo(question_state.current_card)).classes(
                "h-8 hover:shadow"
            ).tooltip("Report a typo")

        ui.space()

        with ui.button_group().props("flat").classes("h-8"):
            ui.button(icon="chevron_right", on_click=lambda: record_score(0)).classes(
                "h-8 hover:shadow"
            ).tooltip("Next card")


def reveal_answer() -> None:
    """Display the card's explanation and disable the reveal button."""
    global answer_label, reveal_button
    if answer_label:
        answer_label.visible = True
    if reveal_button:
        reveal_button.disable()


def pick_next_card() -> Lexicard | None:
    """Select a new card from the learning buckets and reset the UI.

    Returns:
            The new Lexicard or None if buckets are empty.
    """
    global reveal_button, answer_label
    buckets = get_learning_buckets()
    if not buckets:
        return None

    next_card = buckets.pick_card()
    if next_card:
        question_state.set_card(next_card)
        if reveal_button:
            reveal_button.enable()
        if answer_label:
            answer_label.visible = False

        # Proactively play sound if available
        if next_card.sound != "0":
            auto_play(next_card.sound)

    return next_card


def record_score(points_type: int) -> None:
    """Process learning progress based on user performance.

    Args:
            points_type: 2 for mastery, -1 for failure, 0 for skip.
    """
    global reveal_button, answer_label
    buckets = get_learning_buckets()
    if not buckets or not question_state.current_card:
        return

    if points_type == 2:  # Success
        is_mastered = reveal_button.enabled if reveal_button else False
        if is_mastered:
            daily_score.tally += 2
            buckets.promote(question_state.current_card, high_priority=True)
        else:
            daily_score.tally += 1
            buckets.promote(question_state.current_card)
        pick_next_card()

    elif points_type == -1:  # Failure
        buckets.demote(question_state.current_card)
        if answer_label and not answer_label.visible:
            reveal_answer()
            ui.timer(3, pick_next_card, once=True)
        else:
            pick_next_card()

    elif points_type == 0:  # Skip
        pick_next_card()

    notify_dev(f"Score updated to {daily_score.tally}")


@ui.page("/page_mode_single")
async def mode_single_page(client: Client) -> None:
    """Render the single-card practice interface."""
    global answer_label
    await client.connected()

    deck = get_deck()
    if not deck:
        display_message("Redirecting to deck selection...")
        await asyncio.sleep(2)
        ui.navigate.to("/page_deck")
        return

    # Load initial card
    buckets = get_learning_buckets()
    if buckets:
        initial_card = buckets.get_current_card()
        if initial_card:
            question_state.set_card(initial_card)

    with frame("Practice: Single Mode"):
        display_text("What does this mean?")
        add_practice_command_bar()

        # Main Content
        ui.label(question_state.target_word).classes("text-h2").bind_text_from(question_state, "target_word")
        ui.label(question_state.phonetic).classes("text-h5 italic").bind_text_from(question_state, "phonetic")

        # Audio Control
        with ui.row().classes("items-center mt-4"):

            def play_current():
                if question_state.sound != "0":
                    auto_play(question_state.sound)

            ui.button(icon="volume_up", on_click=play_current).props("flat round").tooltip("Play audio")

        ui.separator().classes("my-6 w-32")

        # Explanation / Answer
        answer_label = ui.label(question_state.explain).classes("text-h4 text-primary centered-wrapped-text")
        answer_label.bind_text_from(question_state, "explain")
        answer_label.visible = False
