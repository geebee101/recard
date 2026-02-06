#!/usr/bin/env -S uv run --script
"""Main entry point for the Lexicard application.

This script initializes the NiceGUI application, sets up routes,
handles global exceptions, and starts the web server.
"""

import traceback
from pathlib import Path

from fastapi import Request, Response
from nicegui import Client, app, ui
from nicegui.page import page

# Local imports for pages and logic
from . import (
    auth,  # Injects authentication middleware
    page_about,
    page_blank,
    page_deck,
    page_home,
    page_mode_audio,
    page_mode_missing,
    page_mode_multi,
    page_mode_single,
    page_profile,
)
from .front_commons import (
    ASSETS_DIR,
    add_custom_styles,
    auto_play,
    display_message,
    display_text,
    frame,
)


def create_dynamic_pages() -> None:
    """Register dynamic routes and page definitions."""

    @ui.page("/a")
    async def page_a(client: Client) -> None:
        """Render a simple test page (Page A)."""
        await client.connected()
        with frame("- Page A -"):
            display_message("Page A")
            ui.label("This page is defined in a function.")
            for _ in range(30):
                ui.label("...")
            ui.label("The end. (Scroll area behavior notes in TODO)")
            ui.row()
            display_text("Debug: index of URLs")
            for url in app.urls:
                ui.link(url, target=url)


add_custom_styles()
create_dynamic_pages()


class ClassExample:
    """Example of a page defined within a class context."""

    def __init__(self) -> None:
        """Initialize the class and define its associated web page."""

        @ui.page("/b")
        async def page_b(client: Client) -> None:
            """Render a test page (Page B) with audio capability."""
            await client.connected()
            with frame("- Page B -", but_back):
                auto_play("ขนม")
                display_message("Page B")
                ui.label("This page is defined in a class.")

                # Explicit audio control button
                audio_path = ASSETS_DIR / "ขนม.mp3"
                audio_control = ui.audio(str(audio_path))
                audio_control.set_visibility(False)
                ui.button(icon="volume_up", on_click=audio_control.play)

        def but_back() -> None:
            """Render a back button for Page B."""
            ui.button("back from B", on_click=ui.navigate.back)


ClassExample()


@app.exception_handler(404)
async def exception_handler_404(request: Request, exception: Exception) -> Response:
    """Handle 404 Not Found errors with a custom styled page.

    Args:
            request: The incoming request that failed.
            exception: The 404 exception raised.

    Returns:
            A NiceGUI client response with a 404 status.
    """
    stack_trace = traceback.format_exc()
    msg_to_user = f"**{exception}**\n\nStack trace: \n<pre>{stack_trace}"

    with Client(page(""), request=request) as client:
        with frame("Error"):
            display_message("Sorry, this page does not exist")
            display_text(f"{request.url}")
            ui.button("Back", on_click=ui.navigate.back)
            ui.row()
            display_text("Debug: index of URLs")
            for url in app.urls:
                ui.link(url, target=url)
            ui.markdown(msg_to_user).classes("message")

    return client.build_response(request, 404)


def main() -> None:
    """Main entry point for the application script."""
    # storage_secret is required for session-based storage
    ui.run(title="Lexicard", storage_secret="SECURE_RANDOM_SECRET_KEY", reload=False, port=8080)  # IGNORE: PROTOTYPE ONLY
