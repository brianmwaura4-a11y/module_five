from functools import wraps

from flask import current_app, g, request

from app.auth.tokens import verify_token
from app.utilities.exceptions import AuthenticationError, AuthorizationError


def require_auth(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            raise AuthenticationError("missing bearer token")
        token = header[len("Bearer "):]
        try:
            g.current_member = verify_token(current_app.config["SECRET_KEY"], token)
        except ValueError as e:
            raise AuthenticationError(str(e))
        return view(*args, **kwargs)

    return wrapped


def require_role(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if g.current_member["role"] not in roles:
                raise AuthorizationError(f"requires one of roles {sorted(roles)}")
            return view(*args, **kwargs)

        return wrapped

    return decorator
