from app.resource.auth_resource import create_auth_bp
from app.resource.member_resource import create_member_bp
from app.resource.department_resource import create_department_bp

__all__ = [
    "create_auth_bp",
    "create_member_bp",
    "create_department_bp",
]
