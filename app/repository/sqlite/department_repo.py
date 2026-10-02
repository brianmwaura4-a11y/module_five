from typing import List, Optional

from app.record import Record
from app.repository.interface.department import DepartmentInterfaceRepo
from app.repository.sqlite.base import SQLiteBaseRepository
from app.data.sql_loader import department_sql


class DepartmentRepository(SQLiteBaseRepository, DepartmentInterfaceRepo):
    table = "dept"
    columns = ("id", "name", "is_active")

    def get_by_id(self, record_id: str) -> Optional[Record]:
        """Fetch a single department by its primary key."""
        return self._fetchone(department_sql["get_by_id"], (record_id,))

    def get_by_name(self, name: str) -> Optional[Record]:
        """Fetch a department by its exact name."""
        return self._fetchone(department_sql["get_by_name"], (name,))

    def get_all(self, limit: int = 20, offset: int = 0) -> List[Record]:
        """List departments with pagination."""
        return self._fetchall(department_sql["get_all"], (limit, offset))

    def get_children(self, parent_id: str) -> List[Record]:
        """Fetch direct children of a given department."""
        return self._fetchall(department_sql["get_children"], (parent_id,))

    def get_roots(self) -> List[Record]:
        """Fetch all top-level departments (no parent)."""
        return self._fetchall(department_sql["get_roots"])

    def create(self, data: Record) -> Record:
        """Insert a new department and return the created row."""
        params = (
            data["id"],
            data["name"],
            data.get("parent_id"),
            int(data.get("is_active", True)),
        )
        row = self._conn.execute(department_sql["insert"], params).fetchone()
        self._conn.commit()
        return self._to_dict(row)

    def update(self, record_id: str, data: Record) -> Optional[Record]:
        """Partially update a department and return the updated row."""
        is_active = data.get("is_active")
        params = (
            data.get("name"),
            data.get("parent_id"),
            int(is_active) if is_active is not None else None,
            record_id,
        )
        row = self._conn.execute(department_sql["update"], params).fetchone()
        self._conn.commit()
        return self._to_dict(row) if row else None

    def delete(self, record_id: str) -> bool:
        """Delete a department by ID. Returns True if a row was removed."""
        cur = self._execute(department_sql["delete"], (record_id,))
        return cur.rowcount > 0
