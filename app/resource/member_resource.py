from flask import Blueprint, request

from app.auth.decorators import require_auth, require_role
from app.utilities.pagination import get_pagination
from app.utilities.responses import api_response


def create_member_bp(member_service):
    bp = Blueprint("members", __name__, url_prefix="/api/v2/members")

    @bp.route("", methods=["GET"])
    @require_auth
    def list_members():
        limit, offset = get_pagination()
        data = member_service.list_all(limit, offset)
        total = member_service.count()
        return api_response(
            data=data,
            message="OK",
            meta={"limit": limit, "offset": offset, "total": total},
        )

    @bp.route("", methods=["POST"])
    @require_auth
    @require_role("admin", "manager")
    def create_member():
        data = request.get_json(silent=True) or {}
        result = member_service.create(data)
        return api_response(data=result, message="Created", status_code=201)

    @bp.route("/search", methods=["POST"])
    @require_auth
    def search_members():
        filters = request.get_json(silent=True) or {}
        limit, offset = get_pagination()
        data = member_service.search(filters, limit, offset)
        total = member_service.count_search(filters)
        return api_response(
            data=data,
            message="OK",
            meta={"limit": limit, "offset": offset, "total": total},
        )

    @bp.route("/<record_id>", methods=["GET"])
    @require_auth
    def get_member(record_id: str):
        data = member_service.get_one(record_id)
        return api_response(data=data, message="OK")

    @bp.route("/<record_id>", methods=["PATCH"])
    @require_auth
    @require_role("admin", "manager")
    def update_member(record_id: str):
        data = request.get_json(silent=True) or {}
        result = member_service.update(record_id, data)
        return api_response(data=result, message="Updated")

    @bp.route("/<record_id>", methods=["DELETE"])
    @require_auth
    @require_role("admin")
    def delete_member(record_id: str):
        member_service.delete(record_id)
        return api_response(
            data={"deleted": True, "id": record_id},
            message="Deleted",
        )

    return bp
