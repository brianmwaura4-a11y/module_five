-- name: get_by_id
SELECT id, name, parent_id, is_active
FROM dept
WHERE id = ?;

-- name: get_by_name
SELECT id, name, parent_id, is_active
FROM dept
WHERE name = ?;

-- name: get_all
SELECT id, name, parent_id, is_active
FROM dept
ORDER BY name
LIMIT ? OFFSET ?;

-- name: get_children
SELECT id, name, parent_id, is_active
FROM dept
WHERE parent_id = ?
ORDER BY name;

-- name: get_roots
SELECT id, name, parent_id, is_active
FROM dept
WHERE parent_id IS NULL
ORDER BY name;

-- name: insert
INSERT INTO dept (id, name, parent_id, is_active)
VALUES (?, ?, ?, ?)
RETURNING id, name, parent_id, is_active;

-- name: update
UPDATE dept
SET name      = COALESCE(?, name),
    parent_id = COALESCE(?, parent_id),
    is_active = COALESCE(?, is_active)
WHERE id = ?
RETURNING id, name, parent_id, is_active;

-- name: delete
DELETE FROM dept WHERE id = ?;
