from flask import request


def get_pagination(default_limit: int = 20, max_limit: int = 100):
    # Read query-string parameters from the current request.
    limit = request.args.get("limit", default_limit, type=int)
    offset = request.args.get("offset", 0, type=int)

    # Guard against nonsensical or abusive values.
    if limit < 1:
        limit = default_limit
    if limit > max_limit:
        limit = max_limit
    if offset < 0:
        offset = 0

    return limit, offset
    