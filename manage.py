#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "A2A.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
