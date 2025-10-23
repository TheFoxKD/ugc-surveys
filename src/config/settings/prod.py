from .base import *  # noqa: F403 - Wildcard import необходим для наследования всех базовых настроек Django
from .base import ALLOWED_HOSTS, env

# Prod settings (Docker on remote)
DEBUG = env.bool("DEBUG", default=False)

if not ALLOWED_HOSTS:
    msg = "ALLOWED_HOSTS is required in production"
    raise RuntimeError(msg)
