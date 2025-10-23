from .base import *  # noqa: F403 - Wildcard import необходим для наследования всех базовых настроек Django
from .base import env

# Dev settings (Docker)
DEBUG = env.bool("DEBUG", default=True)

# Allow all hosts in dev unless overridden
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
