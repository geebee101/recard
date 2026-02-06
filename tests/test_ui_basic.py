from nicegui.testing import User

async def test_unauthorized_access(user: User):
    await user.open('/page_profile') # restricted page
    # Should be redirected to login
    await user.should_see('Login with your Atmosphere account')
    await user.should_see('Username')

async def test_login_logout(user: User):
    await user.open('/login')
    await user.should_see('Login with your Atmosphere account')
    
    # Fill username
    user.find('Username').type('toto')
    user.find('Log in').click()
    
    # Check if redirected to home
    await user.should_see('Hello toto!')
    await user.should_see('This is the home page.')
    
    # Logout
    user.find('Logout').click()
    await user.should_see('Login with your Atmosphere account')

async def test_about_page(user: User):
    # Log in first
    await user.open('/login')
    user.find('Username').type('toto')
    user.find('Log in').click()
    await user.should_see('Hello toto!')
    
    # Go to about
    await user.open('/page_about')
    await user.should_see('Lexicard a.k.a. pre-recard.social')
    await user.should_see('An SRS-type app')
