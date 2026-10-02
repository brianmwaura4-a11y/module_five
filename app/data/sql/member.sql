-- name: get_by_id
SELECT id, first_name, last_name, email, password_hash,
       employee_id, dept_id, role, is_active
FROM member
WHERE id = ?;

-- name: get_by_email
SELECT id, first_name, last_name, email, password_hash,
       employee_id, dept_id, role, is_active
FROM member
WHERE email = ?;

-- name: get_all
SELECT id, first_name, last_name, email, employee_id, dept_id, role, is_active
FROM member
ORDER BY last_name, first_name, id
LIMIT ? OFFSET ?;

-- name: insert
INSERT INTO member (
    id, first_name, last_name, email, password_hash,
    employee_id, dept_id, role, is_active
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
RETURNING id, first_name, last_name, email, employee_id, dept_id, role, is_active;

-- name: update
UPDATE member
SET first_name    = COALESCE(?, first_name),
    last_name     = COALESCE(?, last_name),
    email         = COALESCE(?, email),
    password_hash = COALESCE(?, password_hash),
    employee_id   = COALESCE(?, employee_id),
    dept_id       = COALESCE(?, dept_id),
    role          = COALESCE(?, role),
    is_active     = COALESCE(?, is_active)
WHERE id = ?
RETURNING id, first_name, last_name, email, employee_id, dept_id, role, is_active;

-- name: delete
DELETE FROM member WHERE id = ?;
