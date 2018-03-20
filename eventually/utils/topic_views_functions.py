"""
Topic view helper functions
================

This module provides helper functions for all Topic's views functions.
"""
from authentication.models import CustomUser
from topic.models import Topic


def find_mentors_topics(mentor_id):
    """
    Function that have to find topics that belong to the certain mentor.

    :param mentor_id: id of the certain mentor.
    :type mentor_id: int

    :return: list with topics.
    """
    mentor = CustomUser.get_by_id(mentor_id)
    topics = Topic.get_mentors_topics(mentor.id)
    return topics
