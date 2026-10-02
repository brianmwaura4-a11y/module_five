from abc import ABC, abstractmethod
from typing import List, Optional

from app.record import Record


class ReadInterfaceRepo(ABC):
    @abstractmethod
    def get_by_id(self, record_id: str) -> Optional[Record]: ...

    @abstractmethod
    def get_all(self, limit: int = 20, offset: int = 0) -> List[Record]: ...

    @abstractmethod
    def count(self) -> int: ...


class WriteInterfaceRepo(ABC):
    @abstractmethod
    def create(self, data: Record) -> Record: ...

    @abstractmethod
    def update(self, record_id: str, data: Record) -> Optional[Record]: ...

    @abstractmethod
    def delete(self, record_id: str) -> bool: ...


class CrudInterfaceRepo(ReadInterfaceRepo, WriteInterfaceRepo):
    pass
