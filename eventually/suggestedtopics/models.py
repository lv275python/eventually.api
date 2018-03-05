"""
SuggestedTopics module.
==============

This module implements class that represents the suggested topics entity.
"""
import pickle
from django.db import models, IntegrityError
from django.conf import settings
from django.core.cache import cache
from utils.abstractmodel import AbstractModel
from utils.utils import LOGGER
from authentication.models import CustomUser

CACHE_TTL = settings.CACHE_TTL


class SuggestedTopics(AbstractModel):
    """
     Describing of suggested topics entity.

        Attributes:
            :param name: Name of the certain topic.
            :type name: string

            :param description: Describing topic
            :type description: string

            :param owner: Foreign key on the CustomUser that create a topic
            :type owner: int

            :param interested_users: List of CustomUseers that interested in that topic
            :type interested_users: list

            :param created_at: The date when the
            certain topic was created.
            :type created_at: datatime

            :param updated_at: The date when the certain
            topic was last time edited.
            :type updeted_at: datatime
        """

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    owner = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    interested_users = models.ManyToManyField(CustomUser, related_name='interested_users')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


    def to_dict(self):
        """
        Method that converts SuggestedTopics object to dictionary.

        :return: dictionary with suggested topic's information

        :Example:

        | {
        |    'id': 17,
        |    'name': 'My awesome name',
        |    'owner': 8,
        |    'interested_users': []
        |    'description': 'My awesome description',
        |    'created_at': 1509540116,
        |    'updated_at': 1509540116
        | }
        """

        interested_users = [user.id for user in self.interested_users.all()] if self.interested_users else []

        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'owner': self.owner.id,
                'interested_users': interested_users,
                'created_at': int(self.created_at.timestamp()),
                'updated_at': int(self.updated_at.timestamp())
                }

    @staticmethod
    def create(owner, name, description):
        """
        Static method that creates instance of SuggestedTopics class and creates database
        row with the accepted info.

        :param owner: Foreign key on the CustomUser that create a topic
        :type owner: int

        :param name: Name of the certain suggested topic.
        :type name: string

        :param description: Describing suggested topic.
        :type description: string

        :return: suggested topic object or None if topic have not created
        """

        suggested_topic = SuggestedTopics()
        suggested_topic.name = name
        suggested_topic.description = description
        suggested_topic.owner = owner

        try:
            suggested_topic.save()
            return suggested_topic
        except (ValueError, IntegrityError):
            LOGGER.error('Inappropriate value or relational integrity fail')

    def update(self, name=None, description=None, interested_user=None):
        """
        Method that updates SuggestedTopics object according to the accepted info.

        :param name: Name of the certain suggested topic.
        :type name: string

        :param description: Describing suggested topic
        :type description: string

        :param interested_user: List os users id interested in topic
        :type interested_user: list of int

        :return: None
        """

        if name:
            self.name = name
        if description:
            self.description = description
        if interested_user:
            self.add_interested_user(interested_user)
        self.save()
        redis_key = 'suggested_topic_by_id_{0}'.format(self.id)
        if redis_key in cache:
            cache.delete(redis_key)

    @staticmethod
    def get_all():
        """
        Method that returns querysets of all suggested topics
        """
        redis_key = "all_suggested_topics"
        if redis_key in cache:
            all_suggested_topics = cache.get(redis_key)
            all_suggested_topics = pickle.loads(all_suggested_topics)
            return all_suggested_topics
        all_suggested_topics = SuggestedTopics.objects.all()
        cached_topics = pickle.dumps(all_suggested_topics)
        cache.set(redis_key, cached_topics, CACHE_TTL)
        return all_suggested_topics

    def add_interested_user(self, interested_user):
        """
        Method that adds interested users in topic
        """
        if interested_user:
            self.interested_users.add(interested_user)
            redis_key = "interested_users_in_topic_{0}".format(self.id)
            if redis_key in cache:
                cache.delete(redis_key)
            if "all_suggested_topics" in cache:
                cache.delete("all_suggested_topics")
