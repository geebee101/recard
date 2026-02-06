from nicegui import ui
from nicegui.testing import User

async def login(user: User):
    await user.open('/login')
    user.find('Username').type('toto')
    user.find('Log in').click()
    await user.should_see('Hello toto!')



async def test_multi_mode_page(user: User):
    await login(user)
    await user.open('/page_mode_multi')
    await user.should_see('Select the correct translation')
    
    # Check for volume button or other elements
    await user.should_see('volume_up')
