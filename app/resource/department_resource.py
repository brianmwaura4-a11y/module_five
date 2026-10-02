from flask import Blueprint, request

from app.auth.decorators import require_auth, require_role
from app.utilities.pagination import get_pagination
from app.utilities.responses import api_response


def create_department_bp(dept_service):
    bp = Blueprint("departments", __name__, url_prefix="/api/v2/departments")

    @bp.route("", methods=["GET"])
    @require_auth
    def list_departments():
        limit, offset = get_pagination()
        data = dept_service.list_all(limit, offset)
        total = dept_service.count()
        return api_response(
            data=data,
            message="OK",
            meta={"limit": limit, "offset": offset, "total": total},
        )

    @bp.route("", methods=["POST"])
    @require_auth
    @require_role("admin")
    def create_department():
        data = request.get_json(silent=True) or {}
        result = dept_service.create(data)
        return api_response(data=result, message="Created", status_code=201)

    @bp.route("/hierarchy", methods=["GET"])
    @require_auth
    def get_hierarchy():
        data = dept_service.hierarchy()
        return api_response(data=data, message="OK")

    @bp.route("/<record_id>", methods=["GET"])
    @require_auth
    def get_department(record_id: str):
        data = dept_service.get_one(record_id)
        return api_response(data=data, message="OK")

    @bp.route("/<record_id>", methods=["PATCH"])
    @require_auth
    @require_role("admin")
    def update_department(record_id: str):
        data = request.get_json(silent=True) or {}
        result = dept_service.update(record_id, data)
        return api_response(data=result, message="Updated")

    @bp.route("/<record_id>", methods=["DELETE"])
    @require_auth
    @require_role("admin")
    def delete_department(record_id: str):
        dept_service.delete(record_id)
        return api_response(
            data={"deleted": True, "id": record_id},
            message="Deleted",
        )

    return bp
