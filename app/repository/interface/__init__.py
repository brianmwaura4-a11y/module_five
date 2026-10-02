from app.repository.interface.base import (
    ReadInterfaceRepo,
    WriteInterfaceRepo,
    CrudInterfaceRepo,
)
from app.repository.interface.member import MemberInterfaceRepo
from app.repository.interface.department import DepartmentInterfaceRepo


__all__ = [
    "ReadInterfaceRepo",
    "WriteInterfaceRepo",
    "CrudInterfaceRepo",
    "MemberInterfaceRepo",
    "DepartmentInterfaceRepo",
]
