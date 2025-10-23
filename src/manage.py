#!/usr/bin/env python
import os
import sys


def main() -> None:
    """Run administrative tasks."""
    if not os.environ.get("DJANGO_SETTINGS_MODULE"):
        msg = """
        DJANGO_SETTINGS_MODULE is not set.
        Export it to 'config.settings.dev' or 'config.settings.prod'
        """
        raise RuntimeError(msg)
    try:
        from django.core.management import execute_from_command_line  # noqa: PLC0415 I001
    except ImportError as exc:
        msg = """
        Couldn't import Django. Are you sure it's installed and
        available on your PYTHONPATH environment variable? Did you
        forget to activate a virtual environment?
        """
        raise ImportError(msg) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
