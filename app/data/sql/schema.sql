PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS dept (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    parent_id   TEXT REFERENCES dept(id) ON DELETE SET NULL,
    is_active   INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS member (
    id            TEXT PRIMARY KEY,
    first_name    TEXT NOT NULL,
    last_name     TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    employee_id   TEXT,
    dept_id       TEXT REFERENCES dept(id) ON DELETE SET NULL,
    role          TEXT NOT NULL DEFAULT 'employee'
                    CHECK (role IN ('admin', 'manager', 'employee')),
    is_active     INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_member_dept ON member(dept_id);
CREATE INDEX IF NOT EXISTS idx_member_role ON member(role);
CREATE INDEX IF NOT EXISTS idx_dept_parent ON dept(parent_id);
