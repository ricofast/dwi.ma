from ninja.errors import HttpError


def require_auth(request):
    if not request.user.is_authenticated:
        raise HttpError(401, "Authentication required")
    return request.user
