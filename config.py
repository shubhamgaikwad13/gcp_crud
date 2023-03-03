# pylint: disable=too-few-public-methods
import os
import logging
from enum import Enum
from typing import Type
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# The Root Directory of the project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Environment
ENV_DIR = os.path.join(ROOT_DIR, "env/")

app_env = os.getenv("APP_ENV", None)

if app_env:
    logger.info("Loading %s enviroment.", app_env)
    ENV_FILE_PATH = os.path.join(ENV_DIR, ".env." + app_env.lower())
else:
    ENV_FILE_PATH = os.path.join(ENV_DIR, ".env.local")

load_dotenv(ENV_FILE_PATH, verbose=True)


class EnvEnum(Enum):
    DEVELOPMENT = "development"
    STAGE = "stage"
    PRODUCTION = "production"
    TESTING = "testing"
    LOCAL = "local"


class BaseConfig:
    APP_NAME = "Flask Restplus API"
    SECRET_KEY = os.getenv("SECRET_KEY", "JF_SECRET_KEY")
    FLASK_ENV = os.environ.get("FLASK_ENV", EnvEnum.DEVELOPMENT.value)
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 5000))

    LOG_PATH = os.environ.get("LOG_PATH", "logs/logfile.log")

    if app_env in ["prod", "stage"]:
        pass

    else:
        MONGODB_SETTINGS = {'host': 'mongodb://127.0.0.1:27017/gcp_crud'}


class DevelopmentConfig(BaseConfig):
    DEBUG = False
    LOG_LEVEL = logging.DEBUG


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):

    DEBUG = True
    LOG_LEVEL = logging.ERROR


class LocalConfig(BaseConfig):
    DEBUG = True
    LOG_LEVEL = logging.ERROR


def _configuration() -> Type[BaseConfig]:
    env = BaseConfig.FLASK_ENV

    if env == EnvEnum.DEVELOPMENT.value:
        return DevelopmentConfig
    if env == EnvEnum.TESTING.value:
        return TestConfig
    if env == EnvEnum.PRODUCTION.value:
        return ProductionConfig
    if env == EnvEnum.LOCAL.value:
        return LocalConfig
    raise Exception(f"unknown config type {env}")


Config = _configuration()
