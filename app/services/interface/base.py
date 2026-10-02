from abc import ABC, abstractmethod
from typing import List

from app.record import Record


class ReadInterfaceService(ABC):
    @abstractmethod
    def list_all(self, limit: int = 20, offset: int = 0) -> List[Record]: ...

    @abstractmethod
    def get_one(self, record_id: str) -> Record: ...

    @abstractmethod
    def count(self) -> int: ...


class WriteInterfaceService(ABC):
    @abstractmethod
    def create(self, data: Record) -> Record: ...

    @abstractmethod
    def update(self, record_id: str, data: Record) -> Record: ...

    @abstractmethod
    def delete(self, record_id: str) -> None: ...


class CrudInterfaceService(ReadInterfaceService, WriteInterfaceService):
    pass
    