# auth logic
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nicegui import app

unrestricted_page_routes = {'/login'}


@app.add_middleware
class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_page_routes:
                return RedirectResponse(f'/login?redirect_to={request.url.path}')
        return await call_next(request)