from typing import List

from app.record import Record
from app.repository.interface.base import CrudInterfaceRepo
from app.services.interface.base import CrudInterfaceService
from app.utilities.exceptions import NotFoundError


class BaseCrudService(CrudInterfaceService):
    entity_name: str = "Record"

    def __init__(self, repository: CrudInterfaceRepo):
        self._repo = repository

    def count(self) -> int:
        return self._repo.count()

    def list_all(self, limit: int = 20, offset: int = 0) -> List[Record]:
        return self._repo.get_all(limit, offset)

    def get_one(self, record_id: str) -> Record:
        record = self._repo.get_by_id(record_id)
        if record is None:
            raise NotFoundError(f"{self.entity_name} with id {record_id} not found")
        return record

    def delete(self, record_id: str) -> None:
        if not self._repo.delete(record_id):
            raise NotFoundError(f"{self.entity_name} with id {record_id} not found")
