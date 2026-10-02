from flask import Blueprint, request, jsonify
from app.utilities.response import api_response, valiadtion_error, not_found, server_error


def create_member_blueprint(service):
    members_bp = Blueprint(
        "member", 
        __name__, 
        url_prefix="/api/v1/members")


    @members_bp.route("/", methods=["GET"])
    def list_all_users():
        return jsonify(service.list_all()), 200


    @members_bp.route("/", methods=["POST"])
    def create_user():

        res = service.post_data(request.get_data() or {})
        return res, 201


    @members_bp.route("/<member_id>", methods=["GET"])
    def get_one_user(member_id):
        member = service.get_member(member_id)
        if member is None:
            return jsonify({"error": "Member not found"}), 404
        return jsonify(member), 200

    @members_bp.route("/<member_id>", methods=["PUT", "PATCH"])
    def update_user(member_id):
        payload = request.get_json() or {}
        updated_member = service.update(member_id, payload)

        if updated_member is None:
            return not_found("Member not found")
        return api_response(
            message = "Member successfully update",
            status_code = 200,
            data = updated_member
        )

    @members_bp.route("/<member_id>", methods=["DELETE"])
    def delete_user(member_id):
        res = service.delete(member_id)

        if res is None:
            return not_found("Member not found")
        return api_response(
            message = "Member successfully deleted",
            status_code = 204
        )


    return members_bp
