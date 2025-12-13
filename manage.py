#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')

    # --- Activar HTTPS si se usa el flag --ssl ---
    if '--ssl' in sys.argv:
        sys.argv.remove('--ssl')

        # Configurar runserver para usar SSL
        from django.core.management.commands.runserver import Command as runserver
        runserver.default_addr = '127.0.0.1'
        runserver.default_port = '8443'
        runserver.cert_file = 'ssl.crt'
        runserver.key_file = 'ssl.key'

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
