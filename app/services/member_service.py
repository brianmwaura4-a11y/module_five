from typing import List

from app.auth.passwords import hash_password
from app.models import Member
from app.record import Record
from app.repository.interface.department import DepartmentInterfaceRepo
from app.repository.interface.member import MemberInterfaceRepo
from app.services.base_service import BaseCrudService
from app.utilities.exceptions import ConflictError, NotFoundError, ValidationError


class MemberService(BaseCrudService):
    entity_name = "Member"

    def __init__(
        self,
        repository: MemberInterfaceRepo,
        department_repository: DepartmentInterfaceRepo,
    ):
        super().__init__(repository)
        self._dept_repo = department_repository

    @staticmethod
    def _public(record: Record) -> Record:
        d = dict(record)
        d.pop("password_hash", None)
        return d

    def get_one(self, record_id: str) -> Record:
        return self._public(super().get_one(record_id))

    def list_all(self, limit: int = 20, offset: int = 0) -> List[Record]:
        return [self._public(r) for r in super().list_all(limit, offset)]

    def search(
        self, filters: Record, limit: int = 20, offset: int = 0
    ) -> List[Record]:
        return [self._public(r) for r in self._repo.search(filters, limit, offset)]

    def count_search(self, filters: Record) -> int:
        return self._repo.count_search(filters)

    def _validate_dept(self, dept_id) -> None:
        if dept_id is not None and not self._dept_repo.get_by_id(dept_id):
            raise ValidationError(
                f"dept_id {dept_id} does not reference an existing department"
            )

    def create(self, data: Record) -> Record:
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "employee")
        employee_id = data.get("employee_id")
        dept_id = data.get("dept_id")

        if not first_name or not last_name or not email or not password:
            raise ValidationError(
                "first_name, last_name, email, and password are required"
            )
        if self._repo.get_by_email(email):
            raise ConflictError("email already exists")
        self._validate_dept(dept_id)
        try:
            member = Member(
                first_name=first_name,
                last_name=last_name,
                email=email,
                role=role,
                employee_id=employee_id,
                dept_id=dept_id,
                password_hash=hash_password(password),
            )
        except ValueError as e:
            raise ValidationError(str(e))
        return self._public(self._repo.create(member.to_dict()))

    def update(self, record_id: str, data: Record) -> Record:
        allowed = {
            "first_name",
            "last_name",
            "email",
            "employee_id",
            "dept_id",
            "role",
            "is_active",
        }
        filtered = {k: v for k, v in data.items() if k in allowed}

        if "role" in filtered and filtered["role"] not in Member.VALID_ROLES:
            raise ValidationError(f"role must be one of {sorted(Member.VALID_ROLES)}")
        if "dept_id" in filtered:
            self._validate_dept(filtered["dept_id"])
        if "email" in filtered:
            existing = self._repo.get_by_email(filtered["email"])
            if existing and existing["id"] != record_id:
                raise ConflictError("email already in use by another member")
        if data.get("password"):
            filtered["password_hash"] = hash_password(data["password"])

        updated = self._repo.update(record_id, filtered)
        if updated is None:
            raise NotFoundError(f"Member with id {record_id} not found")
        return self._public(updated)

    def delete(self, record_id: str) -> None:
        super().delete(record_id)
