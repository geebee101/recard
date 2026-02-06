"""Authentication middleware for NiceGUI pages.

This module provides a middleware layer that intercepts requests to ensure
users are authenticated before accessing restricted pages.
"""

from collections.abc import Awaitable, Callable

from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import app
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

UNRESTRICTED_ROUTES = {"/login"}


@app.add_middleware
class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware task to restrict access to NiceGUI pages.

    Redirects unauthenticated users to the login page, while allowing
    access to internal NiceGUI routes and specific public routes.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Intercept and validate the authentication status of the incoming request.

        Args:
                request: The incoming FastAPI request object.
                call_next: The next middleware or endpoint handler in the chain.

        Returns:
                A RedirectResponse to /login if unauthenticated, otherwise the response from call_next.
        """
        if not app.storage.user.get("authenticated", False):
            if not request.url.path.startswith("/_nicegui") and request.url.path not in UNRESTRICTED_ROUTES:
                return RedirectResponse(f"/login?redirect_to={request.url.path}")

        return await call_next(request)
