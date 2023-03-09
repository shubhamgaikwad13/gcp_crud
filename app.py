# pylint: disable=redefined-outer-name,unused-variable

import logging
from time import time
import os
from flask_migrate import Migrate
from flask import Flask, g, request, make_response, abort, jsonify
from logzero import logger, loglevel, logfile, formatter
from .config import Config, app_env
from .api.resources.api import api
from .db import mongo_client
from .api.exceptions import AuthException, NoTokenException, ApiException


def _init_logging(app: Flask):
    log = logging.getLogger("werkzeug")
    log.disabled = False
    loglevel(app.config.get("LOG_LEVEL"))
    formatter(logging.Formatter("[%(asctime)s] - %(levelname)s: %(message)s"))

    if app.config.get("FLASK_ENV") != "testing":
        logfile(
            app.config.get("LOG_PATH"),
            maxBytes=10_000_000,
            backupCount=3,
            loglevel=app.config.get("LOG_LEVEL"),
        )


def config_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    return app


def create_app() -> Flask:
    app = config_app()
    app.config["CORS_HEADERS"] = "Content-Type"
    # from api.models.meta import mongo_client
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'./striking-theme-378710-b1a643a7a7b0.json'

    api.init_app(app)
    mongo_client.init_app(app)
    _init_logging(app)

    @app.errorhandler(ApiException)
    def api_exception(error):
        return {"error": str(error)}, error.status_code

    # @app.errorhandler(AuthException)
    # def auth_exception(error):
    #     return {"message": error.message, "details": error.data}, error.status_code

    # @app.errorhandler(NoTokenException)
    # def no_token_exception(error):
    #     print("handling no token exception error")
    #     return {"message": error.message}, error.status_code

    # @app.errorhandler(Exception)
    # def handle_exception(error):
    #     return jsonify({"message": error.message}), error.status_code

    return app


if app_env in ['local']:
    app = create_app()


