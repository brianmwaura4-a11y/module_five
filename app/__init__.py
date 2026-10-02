# Standard library import for reading environment variables
# that control the configuration profile (development, production, testing).
import os

# Loads variables from a local .env file into os.environ before
# the configuration classes are imported and evaluated.
from dotenv import load_dotenv

# The core Flask application class.
from flask import Flask

# Flask-CORS extension handles cross-origin requests, preflight OPTIONS,
# and Access-Control-Allow-* headers automatically.
from flask_cors import CORS

# Configuration dictionary that maps environment names to config classes.
from config import config_by_name

# Database connection factory. Opens SQLite, enables foreign keys,
# sets row_factory, and applies schema.sql on first connect.
from app.data.db import connect

# Concrete SQLite repository implementations.
# These encapsulate all SQL execution and named query loading.
from app.repository.sqlite.department_repo import DepartmentRepository
from app.repository.sqlite.member_repo import MemberRepository

# Blueprint factories from the resource (controller) layer.
# Each function accepts its service, creates a Blueprint, and returns it.
from app.resource.auth_resource import create_auth_bp
from app.resource.department_resource import create_department_bp
from app.resource.member_resource import create_member_bp

# Service layer implementations containing business rules.
from app.services.auth_service import AuthService
from app.services.department_service import DepartmentService
from app.services.member_service import MemberService

# Registers global error handlers so the API always returns JSON
# instead of Flask default HTML error pages.
from app.utilities.error_handlers import register_error_handlers

# Standard JSON response envelope used across all endpoints.
from app.utilities.responses import api_response

# Execute immediately at import time so .env values are available
# before create_app() reads FLASK_CONFIG or FLASK_ENV.
load_dotenv()


def create_app(config_name: str | None = None) -> Flask:
    # ------------------------------------------------------------------
    # 1. Resolve configuration profile
    # ------------------------------------------------------------------
    # If the caller does not pass an explicit profile (e.g. tests),
    # fall back to environment variables. FLASK_CONFIG is checked first,
    # then FLASK_ENV, and finally the hardcoded "default" fallback.
    if config_name is None:
        config_name = (
            os.environ.get("FLASK_CONFIG")
            or os.environ.get("FLASK_ENV", "default")
        )

    # Look up the concrete configuration class. If an unknown name is
    # passed, safely fall back to the default configuration instead of
    # raising a KeyError and crashing on startup.
    config_class = config_by_name.get(config_name, config_by_name["default"])

    # ------------------------------------------------------------------
    # 2. Instantiate Flask and load configuration
    # ------------------------------------------------------------------
    # Create the Flask application instance. __name__ helps Flask locate
    # templates and static files relative to this package if needed.
    app = Flask(__name__)

    # Copy all uppercase attributes from the selected config class into
    # Flask's internal app.config dictionary. After this, values like
    # SECRET_KEY, DATABASE_PATH, and CORS_ALLOWED_ORIGIN are accessible
    # throughout the application via current_app.config or app.config.
    app.config.from_object(config_class)

    # Safety guard for production deployments. The default secret key is
    # only suitable for local development. If an operator starts the app
    # in production without setting a real SECRET_KEY, we fail fast
    # with a clear message rather than silently accepting insecure tokens.
    if config_name == "production" and not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY environment variable must be set in production")

    # ------------------------------------------------------------------
    # 3. Establish database connection
    # ------------------------------------------------------------------
    # connect() opens the SQLite database (file or :memory:), enables
    # foreign key constraints, sets row_factory to sqlite3.Row, and
    # executes schema.sql to create tables and indexes if they do not
    # yet exist. The same connection object is shared across repositories
    # in this simple synchronous setup.
    conn = connect(app.config["DATABASE_PATH"])

    # ------------------------------------------------------------------
    # 4. Build repositories (data access layer)
    # ------------------------------------------------------------------
    # Instantiate the concrete repositories, injecting the SQLite
    # connection. Repositories do not know about HTTP or business rules;
    # they only load named SQL queries and execute them with parameters.
    member_repo = MemberRepository(conn)
    dept_repo = DepartmentRepository(conn)

    # ------------------------------------------------------------------
    # 5. Build services (business logic layer)
    # ------------------------------------------------------------------
    # Services receive repository instances via manual dependency injection.
    # MemberService needs the department repository to validate that a
    # member's dept_id references an existing department.
    member_service = MemberService(member_repo, dept_repo)

    # DepartmentService needs the member repository to block deletion
    # of departments that still have assigned members.
    dept_service = DepartmentService(dept_repo, member_repo)

    # AuthService coordinates signup and login. It needs the member
    # service (to reuse creation logic and validation), the member
    # repository (to access password_hash during login), and the secret
    # key (to sign authentication tokens).
    auth_service = AuthService(
        member_service, member_repo, app.config["SECRET_KEY"]
    )

    # ------------------------------------------------------------------
    # 6. Register HTTP Blueprints (presentation layer)
    # ------------------------------------------------------------------
    # Each factory function creates a Blueprint, closes over its service,
    # defines routes as plain functions, and returns the Blueprint.
    # register_blueprint mounts all routes under their url_prefix.
    app.register_blueprint(create_auth_bp(auth_service))
    app.register_blueprint(create_member_bp(member_service))
    app.register_blueprint(create_department_bp(dept_service))

    # ------------------------------------------------------------------
    # 7. Register global error handlers
    # ------------------------------------------------------------------
    # This attaches handlers for AppException (404, 409, 400, 401, 403),
    # Flask native 404/405, and a catch-all for unexpected exceptions.
    # It guarantees the API always returns the standard JSON envelope.
    register_error_handlers(app)

    # ------------------------------------------------------------------
    # 8. Enable CORS
    # ------------------------------------------------------------------
    # Replaces the old manual after_request CORS header injection.
    # Flask-CORS automatically responds to OPTIONS preflight requests
    # and injects the correct Access-Control-Allow-* headers based on
    # the origins configured in CORS_ALLOWED_ORIGIN.
    CORS(app, origins=app.config["CORS_ALLOWED_ORIGIN"])

    # ------------------------------------------------------------------
    # 9. Health check endpoint
    # ------------------------------------------------------------------
    # A simple liveness probe outside any Blueprint. Load balancers,
    # Docker health checks, and monitoring services can call this to
    # verify the process is running and responsive.
    @app.route("/health")
    def health():
        # Use the standard api_response envelope so the health check
        # follows the same JSON shape as every other endpoint:
        # {"success": true, "message": "OK", "data": {...}, "meta": null}
        return api_response(
            data={
                "status": "Active",
                "service": "hrms-api",
                "version": "1.0.0",
                "env": app.config.get("ENV", config_name),
            },
            message="OK",
        )

    # Return the fully wired application instance to the caller.
    # Callers include run.py (development server), Gunicorn workers,
    # and test fixtures that need an app context.
    return app
    