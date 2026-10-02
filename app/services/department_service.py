from typing import List

from app.models import Department
from app.record import Record
from app.repository.interface.department import DepartmentInterfaceRepo
from app.repository.interface.member import MemberInterfaceRepo
from app.services.base_service import BaseCrudService
from app.utilities.exceptions import ConflictError, NotFoundError, ValidationError


class DepartmentService(BaseCrudService):
    entity_name = "Department"

    def __init__(
        self,
        repository: DepartmentInterfaceRepo,
        member_repository: MemberInterfaceRepo,
    ):
        super().__init__(repository)
        self._member_repo = member_repository

    def create(self, data: Record) -> Record:
        name = data.get("name")
        parent_id = data.get("parent_id")
        if not name:
            raise ValidationError("name is required")
        if self._repo.get_by_name(name):
            raise ConflictError("department name already exists")
        if parent_id and not self._repo.get_by_id(parent_id):
            raise ValidationError(f"parent_id {parent_id} does not exist")
        return self._repo.create(
            Department(name=name, parent_id=parent_id).to_dict()
        )

    def update(self, record_id: str, data: Record) -> Record:
        filtered = {
            k: v for k, v in data.items() if k in ("name", "parent_id", "is_active")
        }
        if "name" in filtered:
            existing = self._repo.get_by_name(filtered["name"])
            if existing and existing["id"] != record_id:
                raise ConflictError("department name already in use")
        if "parent_id" in filtered and filtered["parent_id"]:
            if filtered["parent_id"] == record_id:
                raise ValidationError("department cannot be its own parent")
            if not self._repo.get_by_id(filtered["parent_id"]):
                raise ValidationError("parent department does not exist")
        updated = self._repo.update(record_id, filtered)
        if updated is None:
            raise NotFoundError(f"Department with id {record_id} not found")
        return updated

    def delete(self, record_id: str) -> None:
        if self._member_repo.search({"dept_id": record_id}, limit=1, offset=0):
            raise ConflictError(
                "cannot delete a department that still has members assigned to it"
            )
        if self._repo.get_children(record_id):
            raise ConflictError(
                "cannot delete a department that still has child departments"
            )
        super().delete(record_id)

    def hierarchy(self) -> List[Record]:
        def build(node: Record) -> Record:
            children = self._repo.get_children(node["id"])
            return {**node, "children": [build(c) for c in children]}

        return [build(root) for root in self._repo.get_roots()]
