import sqlite3
from typing import Any, List, Optional, Sequence

from app.record import Record


class SQLiteBaseRepository:
    """Runs SQL passed in by subclasses. Does not own query text."""

    table: str = ""
    columns: Sequence[str] = ()

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def _fetchone(self, sql: str, params: Sequence[Any] = ()) -> Optional[Record]:
        row = self._conn.execute(sql, params).fetchone()
        return self._to_dict(row, strip_password=True)

    def _fetchall(self, sql: str, params: Sequence[Any] = ()) -> List[Record]:
        rows = self._conn.execute(sql, params).fetchall()
        return [self._to_dict(r, strip_password=True) for r in rows]

    def _execute(self, sql: str, params: Sequence[Any] = ()) -> sqlite3.Cursor:
        cur = self._conn.execute(sql, params)
        self._conn.commit()
        return cur

    def count(self) -> int:
        """Return total row count for this repository's table."""
        row = self._conn.execute(f"SELECT COUNT(*) FROM {self.table}").fetchone()
        return row[0] if row else 0

    @staticmethod
    def _to_dict(row, strip_password: bool = True) -> Optional[Record]:
        if row is None:
            return None
        d = dict(row)
        if "is_active" in d:
            d["is_active"] = bool(d["is_active"])
        if strip_password:
            d.pop("password_hash", None)
        return d
