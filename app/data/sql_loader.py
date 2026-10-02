from functools import lru_cache
from pathlib import Path
from typing import Dict

SQL_DIR = Path(__file__).resolve().parent / "sql"


class SqlQuerySet:
    def __init__(self, filename: str):
        self._filename = filename
        self._queries = self._load(filename)

    @staticmethod
    @lru_cache(maxsize=16)
    def _load(filename: str) -> Dict[str, str]:
        path = SQL_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"SQL file not found: {path}")

        queries: Dict[str, str] = {}
        name: str | None = None
        buffer: list[str] = []

        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("-- name:"):
                if name is not None and buffer:
                    queries[name] = "\n".join(buffer).strip()
                name = stripped.split(":", 1)[1].strip()
                buffer = []
            elif name is not None:
                buffer.append(line)

        if name is not None and buffer:
            queries[name] = "\n".join(buffer).strip()

        return queries

    def __getitem__(self, name: str) -> str:
        try:
            return self._queries[name]
        except KeyError as exc:
            raise KeyError(
                f"Query '{name}' not found in {self._filename}. "
                f"Available: {sorted(self._queries)}"
            ) from exc


schema_sql = (SQL_DIR / "schema.sql").read_text(encoding="utf-8")
member_sql = SqlQuerySet("member.sql")
department_sql = SqlQuerySet("department.sql")
