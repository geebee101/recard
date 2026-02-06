from nicegui import ui
from nicegui.testing import User

async def test_click(user: User) -> None:
    await user.open('/')
    await user.should_see('Click me')
    user.find(ui.button).click()
    await user.should_see('Hello World!')