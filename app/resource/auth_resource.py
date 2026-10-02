from flask import Blueprint, request

from app.utilities.responses import api_response


def create_auth_bp(auth_service):
    bp = Blueprint("auth", __name__, url_prefix="/api/v2/auth")

    @bp.route("/login", methods=["POST"])
    def login():
        body = request.get_json(silent=True) or {}
        result = auth_service.login(body.get("email"), body.get("password"))
        return api_response(data=result, message="Logged in")

    @bp.route("/signup", methods=["POST"])
    def signup():
        body = request.get_json(silent=True) or {}
        result = auth_service.signup(body)
        return api_response(data=result, message="Signed up", status_code=201)

    return bp
