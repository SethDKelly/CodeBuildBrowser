from flask import render_template, request
import logging


def register_error_handlers(app):
    """Register global error handlers on the Flask `app`.

    Keeps error handling centralized (templates in `templates/`).
    """
    logger = logging.getLogger(__name__)

    @app.errorhandler(404)
    def _handle_404(e):
        logger.info("404: %s", request.path)
        return render_template("error404.html"), 404

    @app.errorhandler(410)
    def _handle_410(e):
        logger.info("410: %s", request.path)
        return render_template("error410.html"), 410

    @app.errorhandler(500)
    def _handle_500(e):
        logger.exception("500 internal server error on %s", request.path)
        return render_template("error500.html"), 500
