#!/usr/bin/env python
# importing base packages to add apps to the field of view
import os 
import sys

# base file name, not to run any functional from imports
if __name__ == "__main__": 
    #import django settings (ports, etc.)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventually.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
