from app.utilities.exceptions import AppException
from app.utilities.responses import api_response, server_error


def register_error_handlers(app):
    @app.errorhandler(AppException)
    def handle_app_exception(e: AppException):
        return api_response(
            data=e.payload,
            message=e.message,
            success=False,
            status_code=e.status_code,
        )

    @app.errorhandler(404)
    def handle_flask_404(e):
        return api_response(message="Not found", success=False, status_code=404)

    @app.errorhandler(405)
    def handle_flask_405(e):
        return api_response(
            message="Method not allowed",
            success=False,
            status_code=405,
        )

    @app.errorhandler(Exception)
    def handle_unexpected(e):
        app.logger.exception(e)
        return server_error()
