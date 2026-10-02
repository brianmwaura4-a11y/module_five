from abc import abstractmethod
from typing import List, Optional

from app.record import Record
from app.repository.interface.base import CrudInterfaceRepo


class DepartmentInterfaceRepo(CrudInterfaceRepo):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Record]: ...

    @abstractmethod
    def get_children(self, parent_id: str) -> List[Record]: ...

    @abstractmethod
    def get_roots(self) -> List[Record]: ...
