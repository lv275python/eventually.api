"""
Topic view module
================

The module that provides basic logic for getting, creating, updating and deleting
of topic's model objects.
"""

from django.views.generic.base import View


class TopicView(View):
    """
    Item view that handles GET, POST, PUT, DELETE requests and provides appropriate
    operations with topic model.
    """
