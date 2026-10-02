from typing import List, Optional

from app.record import Record
from app.repository.interface.member import MemberInterfaceRepo
from app.repository.sqlite.base import SQLiteBaseRepository
from app.data.sql_loader import member_sql

SEARCHABLE_COLUMNS = frozenset({"dept_id", "role", "is_active"})


class MemberRepository(SQLiteBaseRepository, MemberInterfaceRepo):
    table = "member"
    columns = (
        "id",
        "first_name",
        "last_name",
        "email",
        "employee_id",
        "dept_id",
        "role",
        "is_active",
        "password_hash",
    )

    def get_by_id(self, record_id: str) -> Optional[Record]:
        return self._fetchone(member_sql["get_by_id"], (record_id,))

    def get_by_email(self, email: str) -> Optional[Record]:
        row = self._conn.execute(
            member_sql["get_by_email"], (email,)
        ).fetchone()
        return dict(row) if row else None

    def get_all(self, limit: int = 20, offset: int = 0) -> List[Record]:
        return self._fetchall(member_sql["get_all"], (limit, offset))

    def create(self, data: Record) -> Record:
        params = (
            data["id"],
            data["first_name"],
            data["last_name"],
            data["email"],
            data["password_hash"],
            data.get("employee_id"),
            data.get("dept_id"),
            data.get("role", "employee"),
            int(data.get("is_active", True)),
        )
        row = self._conn.execute(member_sql["insert"], params).fetchone()
        self._conn.commit()
        return self._to_dict(row)

    def update(self, record_id: str, data: Record) -> Optional[Record]:
        is_active = data.get("is_active")
        params = (
            data.get("first_name"),
            data.get("last_name"),
            data.get("email"),
            data.get("password_hash"),
            data.get("employee_id"),
            data.get("dept_id"),
            data.get("role"),
            int(is_active) if is_active is not None else None,
            record_id,
        )
        row = self._conn.execute(member_sql["update"], params).fetchone()
        self._conn.commit()
        return self._to_dict(row) if row else None

    def delete(self, record_id: str) -> bool:
        cur = self._execute(member_sql["delete"], (record_id,))
        return cur.rowcount > 0

    def search(self, filters: Record, limit: int = 20, offset: int = 0) -> List[Record]:
        clauses, values = [], []
        for col in SEARCHABLE_COLUMNS:
            if col in filters and filters[col] is not None:
                clauses.append(f"{col} = ?")
                values.append(filters[col])

        if filters.get("last_name_prefix"):
            clauses.append("last_name LIKE ? ESCAPE '\\'")
            escaped = (
                str(filters["last_name_prefix"])
                .replace("\\", "\\\\")
                .replace("%", "\\%")
                .replace("_", "\\_")
            )
            values.append(escaped + "%")

        where = " AND ".join(clauses) if clauses else "1 = 1"
        values.extend([limit, offset])
        sql = (
            "SELECT id, first_name, last_name, email, employee_id, dept_id, role, is_active "
            f"FROM member WHERE {where} "
            "ORDER BY last_name, first_name, id LIMIT ? OFFSET ?"
        )
        return self._fetchall(sql, values)

    def count_search(self, filters: Record) -> int:
        clauses, values = [], []
        for col in SEARCHABLE_COLUMNS:
            if col in filters and filters[col] is not None:
                clauses.append(f"{col} = ?")
                values.append(filters[col])

        if filters.get("last_name_prefix"):
            clauses.append("last_name LIKE ? ESCAPE '\\'")
            escaped = (
                str(filters["last_name_prefix"])
                .replace("\\", "\\\\")
                .replace("%", "\\%")
                .replace("_", "\\_")
            )
            values.append(escaped + "%")

        where = " AND ".join(clauses) if clauses else "1 = 1"
        sql = f"SELECT COUNT(*) FROM member WHERE {where}"
        row = self._conn.execute(sql, values).fetchone()
        return row[0] if row else 0
