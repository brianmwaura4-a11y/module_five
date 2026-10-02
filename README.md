# HRMS API

Flask-based Human Resource Management System API. Provides authenticated access to members, departments, and payroll, with role-based access control and SQLite persistence.

## Overview

| Layer | Responsibility |
|-------|----------------|
| Resource | HTTP routing, authentication, request/response handling |
| Service | Validation and business rules |
| Repository | Data access (raw SQL against SQLite) |
| Model | Domain entities |

Collection and item endpoints use separate MethodView classes so unsupported methods return 405 Method Not Allowed instead of an unhandled error.

## Requirements

- Python 3.10+
- Flask

    pip install flask

## Getting started

    # 1. Bootstrap the first administrator (not exposed over HTTP)
    python seed_admin.py

    # 2. Start the development server
    python -c "from app import create_app; create_app().run(debug=True)"

Verify the service:

    GET /health

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| FLASK_CONFIG | development | development, testing, or production |
| SECRET_KEY | Development fallback | Required when FLASK_CONFIG=production |
| DATABASE_PATH | hrms.db | Path to the SQLite database file |
| CORS_ALLOWED_ORIGIN | * | Value for Access-Control-Allow-Origin |

## API routes

| URL | Class | Methods |
|-----|--------|---------|
| /api/v2/members | MemberCollection | GET, POST, QUERY |
| /api/v2/members/<id> | MemberItem | GET, PATCH, DELETE |
| /api/v2/departments | DepartmentCollection | GET, POST |
| /api/v2/departments/<id> | DepartmentItem | GET, PATCH, DELETE |
| /api/v2/payroll | PayrollCollection | GET, POST |
| /api/v2/payroll/<id> | PayrollItem | GET, PATCH, DELETE |
| /api/v2/auth/login | LoginResource | POST |
| /api/v2/auth/signup | SignupResource | POST |
| /health | - | GET |

## Authentication

Protected endpoints require:

    Authorization: Bearer <token>

Tokens are issued by login and signup. Public endpoints: /api/v1/auth/login, /api/v1/auth/signup, /health.

### Sign up

Creates a member with role employee only. Elevated roles cannot be granted via self-service registration.

    POST /api/v1/auth/signup
    Content-Type: application/json

    {
      "first_name": "Jane",
      "last_name": "Doe",
      "email": "jane@example.com",
      "password": "MySecret1",
      "employee_id": "E-1001",
      "dept_id": null
    }

Response: 201 Created (token payload, same shape as login).

### Login

    POST /api/v1/auth/login
    Content-Type: application/json

    {
      "email": "admin@example.com",
      "password": "your-password"
    }

Response: 200 OK

    {
      "token": "<signed-token>",
      "member_id": "<uuid>",
      "role": "admin"
    }

### Initial administrator

The first admin must be created with the seed script, because protected routes require an existing admin:

    python seed_admin.py

## Members

| Operation | Method | Path | Roles |
|-----------|--------|------|--------|
| List | GET | /api/v2/members | Authenticated |
| Search | QUERY | /api/v2/members | Authenticated |
| Create | POST | /api/v2/members | admin, manager |
| Retrieve | GET | /api/v2/members/<id> | Authenticated |
| Update | PATCH | /api/v2/members/<id> | admin, manager |
| Delete | DELETE | /api/v2/members/<id> | admin |

Query parameters: limit (default 20), offset (default 0).

### Create member

    POST /api/v1/members
    Authorization: Bearer <token>
    Content-Type: application/json

    {
      "first_name": "John",
      "last_name": "Smith",
      "email": "john@example.com",
      "password": "SecurePass9",
      "role": "manager",
      "employee_id": "E-2002",
      "dept_id": "<department-id>"
    }

### Search members

    QUERY /api/v1/members?limit=20&offset=0
    Authorization: Bearer <token>
    Content-Type: application/json

    {
      "dept_id": "<department-id>",
      "role": "employee",
      "is_active": 1,
      "last_name_prefix": "Smi"
    }

Allowed filters: dept_id, role, is_active, last_name_prefix.

### Update member

    PATCH /api/v1/members/<id>
    Authorization: Bearer <token>
    Content-Type: application/json

    {
      "dept_id": "<department-id>",
      "role": "employee",
      "is_active": 0,
      "password": "NewSecret1"
    }

password is optional. Password hashes are never returned in API responses.

## Departments

| Operation | Method | Path | Roles |
|-----------|--------|------|--------|
| List | GET | /api/v2/departments | Authenticated |
| Create | POST | /api/v2/departments | admin |
| Retrieve | GET | /api/v2/departments/<id> | Authenticated |
| Update | PATCH | /api/v2/departments/<id> | admin |
| Delete | DELETE | /api/v2/departments/<id> | admin |

Deletion is rejected while members remain assigned to the department.

### Create department

    POST /api/v1/departments
    Authorization: Bearer <token>
    Content-Type: application/json

    {
      "name": "Engineering"
    }

## Payroll



## Roles

| Capability | employee | manager | admin |
|------------|----------|---------|-------|
| Read members and departments | Yes | Yes | Yes |
| Create / update members | No | Yes | Yes |
| Manage departments | No | No | Yes |
| Manage payroll | No | No | Yes |
| Delete members | No | No | Yes |

## Error responses

| Status | Condition |
|--------|-----------|
| 400 | Validation failure |
| 401 | Missing or invalid credentials / token |
| 403 | Authenticated but insufficient role |
| 404 | Resource not found |
| 405 | HTTP method not allowed on this path |
| 409 | Conflict (e.g. duplicate email, referential constraint) |

    {
      "error": "email already exists"
    }

## Project structure

    .
    ├── config.py
    ├── seed_admin.py
    ├── migrations/
    │   ├── 0001_initial.sql
    │   ├── 0002_add_password_hash.sql
    │   └── 0003_add_payroll.sql
    └── app/
        ├── __init__.py
        ├── cors.py
        ├── error_handlers.py
        ├── exceptions.py
        ├── record.py
        ├── auth/
        ├── data/
        ├── models/
        ├── repository/
        ├── services/
        └── resource/

Schema changes apply automatically on connect via migrations/, recorded in schema_migrations.

## Example workflow

    # Seed administrator
    python seed_admin.py

    # Authenticate
    curl -s -X POST http://127.0.0.1:5000/api/v2/auth/login \
      -H "Content-Type: application/json" \
      -d '{"email":"admin@example.com","password":"..."}'

    # Create a department
    curl -s -X POST http://127.0.0.1:5000/api/v2/departments \
      -H "Authorization: Bearer <token>" \
      -H "Content-Type: application/json" \
      -d '{"name":"Engineering"}'

    # List members
    curl -s http://127.0.0.1:5000/api/v2/members \
      -H "Authorization: Bearer <token>"
      