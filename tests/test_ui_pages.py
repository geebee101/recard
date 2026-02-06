from nicegui.testing import User

async def login(user: User):
    await user.open('/login')
    user.find('Username').type('toto')
    user.find('Log in').click()
    await user.should_see('Hello toto!')

async def test_deck_page_loading(user: User):
    await login(user)
    await user.open('/page_deck')
    await user.should_see('Currently Selected')

    # It should load the default deck if none is selected
    await user.should_see('demodeck')

async def test_profile_page(user: User):
    await login(user)
    await user.open('/page_profile')
    await user.should_see('User Profile')
    await user.should_see('Member since')
    await user.should_see('toto')

async def test_single_mode_page(user: User):
    await login(user)
    await user.open('/page_mode_single')
    # Single mode shows the prompt
    await user.should_see('What does this mean?')
    
    # Try to find the reveal button. 
    await user.should_see('Reveal Answer')
    user.find('Reveal Answer').click()

    
    # Check for the learning buttons
    await user.should_see('Already Known')
    await user.should_see('Mistake')
