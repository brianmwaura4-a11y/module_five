from app.repository.interface.base import CrudInterfaceRepo
from app.repository.interface.member import MemberInterfaceRepo
from app.repository.interface.department import DepartmentInterfaceRepo
from app.repository.sqlite.member_repo import MemberRepository
from app.repository.sqlite.department_repo import DepartmentRepository


__all__ = [
    "CrudInterfaceRepo",
    "MemberInterfaceRepo",
    "DepartmentInterfaceRepo",
    "MemberRepository",
    "DepartmentRepository",
]
