from abc import abstractmethod
from typing import List, Optional

from app.record import Record
from app.repository.interface.base import CrudInterfaceRepo


class MemberInterfaceRepo(CrudInterfaceRepo):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Record]: ...

    @abstractmethod
    def search(self, filters: Record, limit: int = 20, offset: int = 0) -> List[Record]: ...

    @abstractmethod
    def count_search(self, filters: Record) -> int: ...
