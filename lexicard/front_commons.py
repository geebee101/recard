"""Common UI components and state management for the Lexicard frontend.

This module provides common layout frames, navigation elements, and global
state objects used across multiple pages of the application.
"""

from collections.abc import Callable, Generator
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

from nicegui import app, ui
from pydantic import ValidationError
from starlette.responses import RedirectResponse

from .probbucket import ProbBucket

if TYPE_CHECKING:
    from .models import Deck, Lexicard

# Constants and Global state
IS_DEV = True  # Flag for developer mode notifications

# Command bar reference (updated by pages to add context-specific buttons)
command_bar: ui.footer | None = None

# Asset directory relative to this file
ASSETS_DIR = Path(__file__).parent.parent / "assets"


class Tally:
    """A simple observable counter for tracking scores."""

    def __init__(self) -> None:
        """Initialize the tally counter to zero."""
        self.tally: int = 0


# Global instances for session tracking (Note: Not multi-user safe)
daily_score = Tally()
current_deck: Optional["Deck"] = None
learning_buckets: ProbBucket | None = None


def get_command_bar() -> ui.footer | None:
    """Retrieve the current command bar (footer).

    Returns:
            The global footer instance or None.
    """
    return command_bar


def get_deck() -> Optional["Deck"]:
    """Retrieve the current deck from storage or global state.

    Returns:
            The current Deck object or None.
    """
    global current_deck
    from .models import Deck, load_deck_from_json_file, FILE_PATH

    try:
        # Attempt to retrieve from tab-specific storage
        stored_deck = app.storage.tab.get("deck", None)
        if stored_deck:
            if isinstance(stored_deck, dict):
                current_deck = Deck.model_validate(stored_deck)
            else:
                current_deck = stored_deck
            notify_dev(f"Deck loaded from storage: {current_deck.name}", "positive")
        else:
            # Load default if none found
            try:
                current_deck = load_deck_from_json_file(FILE_PATH)
                app.storage.tab.update({"deck": current_deck})
                notify_dev(f"Default deck loaded: {current_deck.name}", "positive")
            except Exception as e:
                print(f"FAILED to load default deck: {e}")
                current_deck = None
                notify_dev("Failed to load default deck", "negative")
        return current_deck
    except (RuntimeError, ValidationError) as e:
        # tab storage is only available with a client connection
        print(f"### Error accessing storage: {e}")
        return None



def get_learning_buckets() -> ProbBucket | None:
    """Obtain the user's probability buckets for the current deck.

    Returns:
            A ProbBucket instance managed globally.
    """
    global learning_buckets
    if learning_buckets:
        return learning_buckets

    learning_buckets = ProbBucket()
    deck = get_deck()
    if deck:
        learning_buckets.add_cards(deck.cards)
    return learning_buckets


def add_custom_styles() -> None:
    """Inject custom CSS into the page for specific text alignment and wrapping."""
    ui.add_css("""
	.centered-wrapped-text {
		text-align: center;
		overflow-wrap: break-word;
		word-wrap: break-word;
		text-wrap: balance;
	}
	.multi-line-notification {
		white-space: pre-line;
	}
	""", shared=True)


@ui.page("/login")
def login(redirect_to: str = "/") -> RedirectResponse | None:
    """Public login page for authentication.

    Args:
            redirect_to: The URL to navigate to after successful login.

    Returns:
            A RedirectResponse if already authenticated.
    """
    passwords = {"toto": "toto"}  # IGNORE: PROTOTYPE ONLY

    def try_login() -> None:
        """Check credentials and update session state."""
        if passwords.get(username.value) == username.value:
            app.storage.user.update({"username": username.value, "authenticated": True})
            ui.navigate.to(redirect_to)
        else:
            ui.notify("Wrong username or password", color="negative")

    if app.storage.user.get("authenticated", False):
        return RedirectResponse("/")

    with ui.column().classes("absolute-center items-center"):
        display_message("Login with your Atmosphere account")
        ui.label("e.g. ny.tngl.sh or my.bsky.social, etc.").classes("text-grey-8 centered-wrapped-text")
        with ui.card():
            username = ui.input("Username").on("keydown.enter", try_login)
            ui.button("Log in", on_click=try_login)
    return None


@contextmanager
def frame(navigation_title: str, buttons_callback: Callable | None = None) -> Generator[None, None, None]:
    """Shared layout frame for all pages.

    Args:
            navigation_title: Title text to display in the header.
            buttons_callback: A function that populates the command bar with buttons.
    """
    global command_bar
    ui.page_title("pre-Recard")

    if not app.storage.user.get("authenticated"):
        # We must yield to satisfy the context manager even if we don't render much
        with ui.column():
                yield
        return


    ui.colors(primary="#9bf8b2", secondary="#53B689", accent="#03300e", positive="#53B689")

    with ui.header(elevated=True).classes("items-center h-10 py-0"):
        with ui.button().props(' flat color=grey round size="sm"').classes("p-0"):
            ui.html("&copy;", sanitize=False)
            with ui.tooltip().classes("bg-brown-3 w-40 text-white"):
                ui.html("&copy; 2026 แรช for newthai", sanitize=False)

        ui.space()

        if deck := get_deck():
            ui.label(f"cards: {len(deck.cards)}")
            ui.badge(0, color="skyblue").props("align: middle").bind_text_from(daily_score, "tally")

        with ui.button(icon="menu").props("flat color=white round"):
            with ui.menu():
                ui.menu_item("Home", on_click=lambda: ui.navigate.to("/"))
                ui.separator()
                with ui.menu_item("TEST SECTION", auto_close=False):
                    with ui.item_section().props("side"):
                        ui.icon("keyboard_arrow_right")
                    with ui.menu().props('anchor="top end" self="top start" auto-close'):
                        ui.menu_item("Ex. page by a function", on_click=lambda: ui.navigate.to("/a"))
                        ui.menu_item("Ex. page by a Class", on_click=lambda: ui.navigate.to("/b"))
                        ui.menu_item("Blank page", on_click=lambda: ui.navigate.to("/page_blank"))
                        ui.menu_item("404", on_click=lambda: ui.navigate.to("/page_non"))
                ui.separator()
                ui.menu_item("Deck page", on_click=lambda: ui.navigate.to("/page_deck"))
                with ui.menu_item("Practice", auto_close=False):
                    with ui.item_section().props("side"):
                        ui.icon("keyboard_arrow_right")
                    with ui.menu().props('anchor="top end" self="top start" auto-close'):
                        ui.menu_item("Mode single", on_click=lambda: ui.navigate.to("/page_mode_single"))
                        ui.menu_item("Mode audio", on_click=lambda: ui.navigate.to("/page_mode_audio"))
                        ui.menu_item("Mode multi", on_click=lambda: ui.navigate.to("/page_mode_multi"))
                        ui.menu_item("Mode missing", on_click=lambda: ui.navigate.to("/page_mode_missing"))
                ui.separator()
                ui.menu_item("Profile", on_click=lambda: ui.navigate.to("/page_profile"))
                ui.separator()
                ui.menu_item("About", on_click=lambda: ui.navigate.to("/page_about"))
                ui.separator()
                ui.menu_item("Logout", on_click=lambda: (app.storage.user.clear(), ui.navigate.to("/login")))

    with ui.footer(fixed=True).classes("items-center h-10 py-0 gap-0 p-0") as ft:
        command_bar = ft
        if buttons_callback:
            buttons_callback()

    with ui.scroll_area().classes("w-full h-[calc(100dvh-7rem)] overflow-y-auto"):
        with ui.column().classes("w-full start items-center justify-center"):
            yield


def display_message(content: str) -> ui.label:
    """Display highly visible header text.

    Args:
            content: The text to display.

    Returns:
            The NiceGUI label object.
    """
    return ui.label(content).classes("text-h4 text-grey-8 centered-wrapped-text")


def display_text(content: str) -> ui.label:
    """Display standard formatted body text.

    Args:
            content: The text to display.

    Returns:
            The NiceGUI label object.
    """
    return ui.label(content).classes("text-grey-8 centered-wrapped-text")


def notify(content: str, notification_type: str | None = None) -> None:
    """Show a notification at the bottom of the screen.

    Args:
            content: The message to show.
            notification_type: Quasar notification type ('negative', 'positive', 'warning').
    """
    ui.notify(
        content,
        position="bottom-left",
        type=notification_type,
        multi_line=True,
        classes="multi-line-notification",
    )


def notify_dev(content: str, notification_type: str | None = None) -> None:
    """Show a development-only notification if IS_DEV is True.

    Args:
            content: The message to show.
            notification_type: Quasar notification type.
    """
    if IS_DEV:
        notify(f"DEV-{content}", notification_type=notification_type)


def report_typo(card: "Lexicard") -> Any:
    """Display a dialog to report a typo on a specific card.

    Args:
            card: The Lexicard object containing the potential typo.

    Returns:
            An awaitable object representing the dialog.
    """
    with ui.context.client.content:
        with ui.dialog() as dialog, ui.card():
            ui.label(f"Typo on {card.target_word if card else 'card'}?").classes("text-h5 text-bold")
            with ui.column().classes("gap-0"):
                typo_spelling = ui.checkbox("Target spelling")
                typo_audio = ui.checkbox("Audio")
                ui.checkbox("Phonetics")
                ui.checkbox("Translation")
            with ui.row():
                ui.button("Cancel", on_click=lambda: dialog.submit("Cancel"))
                ui.button("Report", on_click=lambda: dialog.submit("Report"))

        async def show_result():
            result = await dialog
            if result == "Report":
                report_msg = (
                    f"You reported labels: "
                    f"{typo_spelling.text if typo_spelling.value else ''} "
                    f"{typo_audio.text if typo_audio.value else ''}"
                )
                notify(report_msg)

    return show_result()


def auto_play(filename: str) -> None:
    """Silently load and play an audio file from the assets directory.

    Args:
            filename: The name of the audio file (without .mp3 extension).
    """
    audio_path = ASSETS_DIR / f"{filename}.mp3"
    audio_element = ui.audio(str(audio_path))
    audio_element.set_visibility(False)
    audio_element.play()
