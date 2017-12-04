"""
Item view module
================

The module that provides basic logic for getting, creating, updating and deleting
of item's model objects.
"""

from django.views.generic.base import View


class ItemView(View):
    """
    Item view that handles GET, POST, PUT, DELETE requests and provides appropriate
    operations with item model.
    """
