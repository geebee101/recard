from nicegui.testing import User

async def login(user: User):
    await user.open('/login')
    user.find('Username').type('toto')
    user.find('Log in').click()
    await user.should_see('Hello toto!')


async def test_audio_mode_page(user: User):
    await login(user)
    await user.open('/page_mode_audio')
    await user.should_see('Audio Mode')
    await user.should_see('Listen and identify')

async def test_missing_mode_page(user: User):
    await login(user)
    await user.open('/page_mode_missing')
    await user.should_see('Missing Mode')
    await user.should_see('Identify the target word')

