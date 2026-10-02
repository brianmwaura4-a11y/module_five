from flask import jsonify
from typing import Any, Optional, Dict

def api_response(data = None, message = "OK", success = True, status_code = 200, meta = None):
    payload = {
        "success" : success,
        "message" : message,
        "data" : data if data is not None else "",
        "meta" : meta if meta is not None else "",
    }

    return jsonify(payload), status_code

def validation_error(errors, message = "Validation failed"):
    return api_response(
        data=errors,
        message = message,
        success = False,
        status_code = 422
    )

def not_found(message = "Resource not found"):
    return api_response(
        message = message,
        success = False,
        status_code = 404
    )

def server_error(message = "Internal Server error"):
    return api_response(
        message = message,
        success = False,
        status_code = 500
    )
