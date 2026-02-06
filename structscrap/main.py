#!/usr/bin/env -S uv run --script
# NOPE !/usr/bin/env python3
# import api_router_example
# import class_example
# import function_example
import traceback
import page_home, page_blank
from nicegui import app, ui, Client
from fastapi import Request, Response
from nicegui.page import page
from front_commons import frame, message,text
import auth # force middlware for auth



def auto_play(fname):
    a = ui.audio('../assets/' + fname + '.mp3')
    a.set_visibility(False)
    a.play()

# Example 2: use a function to move the whole page creation into a separate file
def create() -> None:
    @ui.page('/a')
    def page_a():
        with frame('- Page A -'):
            message('Page A')
            ui.label('This page is defined in a function.')
            for i in range(0, 30):
                ui.label('...')
            ui.label('the end TODO: cant get the scroll area to behave')
            ui.row()
            text('Debug: index of URLs')
            for url in app.urls:
                ui.link(url, target=url)
create()

# Example 3: use a class to move the whole page creation into a separate file
class ClassExample:

    def __init__(self) -> None:
        """The page is created as soon as the class is instantiated.

        This can obviously also be done in a method, if you want to decouple the instantiation of the object from the page creation.
        """
        @ui.page('/b')
        def page_b():
            with frame('- Page B -', but_back):
                auto_play('ขนม')
                message('Page B')
                ui.label('This page is defined in a class.')
                # audio with explicit button
                a = ui.audio('../assets/ขนม.mp3')
                a.set_visibility(False)
                ui.button(icon='volume_up', on_click=a.play)

        def but_back():
            ui.button('back from B')
ClassExample()

# Example 4: use APIRouter as described in https://nicegui.io/documentation/page#modularize_with_apirouter
# NOPE app.include_router(api_router_example.router)

@app.exception_handler(404)
async def exception_handler_404(request: Request, exception: Exception) -> Response:
    stack_trace = traceback.format_exc()
    msg_to_user = f"**{exception}**\n\nStack trace: \n<pre>{stack_trace}"
    with Client(page(''), request=request) as client:
        with frame('Error'):
            message('Sorry, this page does not exist')
            text(f'{request.url}')
            ui.button('Back', on_click=ui.navigate.back)
            ui.row()
            text('Debug: index of URLs')
            for url in app.urls:
                ui.link(url, target=url)
            ui.markdown(msg_to_user).classes("message")
    return client.build_response(request, 404)

### UGLY have to manually import all pages
import page_deck, page_about, page_mode_single, page_mode_multi, page_mode_audio, page_mode_missing, page_profile

ui.run(title='Let\'s get started', storage_secret='NO MORE SECRET') 
# WTF RuntimeError: app.storage.user needs a storage_secret passed in ui.run()