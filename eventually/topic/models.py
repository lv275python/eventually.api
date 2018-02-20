"""
Topic module.
==============

This module implements class that represents the topic entity.
"""
# pylint: disable=arguments-differ

from django.db import models, IntegrityError
from authentication.models import CustomUser
from curriculum.models import Curriculum
from utils.abstractmodel import AbstractModel
from utils.utils import LOGGER


class Topic(AbstractModel):
    """
     Describing of topic entity.

        Attributes:
            :param title: Title of the certain topic.
            :type tittle: string

            :param description: Describing topic
            :type description: string

            :param created_at: The date when the
            certain topic was created.
            :type created_at: datatime

            :param updated_at: The date when the certain
            topic was last time edited.
            :type updeted_at: datatime

            :param curriculum: Foreign key on the certain Curriculum model
            :type curriculum: integer

            :param authors: Foreign key on the certain CustomUser model
            :type authors: integer
        """

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(CustomUser, null=True, related_name='topic_author')
    mentors = models.ManyToManyField(CustomUser, related_name='topic_mentors')

    def to_dict(self):
        """
        Method that converts topic object to dictionary.

        :return: dictionary with topic's information

        :Example:

        | {
        |    'id': 17,
        |    'title': 'My awesome title',
        |    'description': 'My awesome description',
        |    'created_at': 1509540116,
        |    'updated_at': 1509540116,
        |    'curriculum' : 13,
        |    'author' : 5,
        |    'mentors' : [21, 33],
        | }
        """

        return {'id': self.id,
                'title': self.title,
                'description': self.description,
                'created_at': int(self.created_at.timestamp()),
                'updated_at': int(self.updated_at.timestamp()),
                'curriculum': self.curriculum.id,
                'author': self.author.id,
                'mentors': sorted([mentor.id for mentor in self.mentors.all()])}

    @staticmethod
    def create(curriculum, author, title=None, description=None, mentors=()):
        """
        Static method that creates instance of Topic class and creates database
        row with the accepted info.

        :param: curriculum: Certain Curriculum's object. Is required.
        :type curriculum: Curriculum model.

        :param: author: Topic's author. Is required.
        :type author: CustomUser model.

        :param title: Title of the certain topic.
        :type title: string

        :param description: Describing topic.
        :type description: string

        :param mentors: Topic's mentors.
        :type description: list

        :return: topic object or None if topic have not created
        """

        topic = Topic()
        topic.curriculum = curriculum
        topic.author = author
        topic.title = title
        topic.description = description

        try:
            topic.save()
            topic.mentors.add(author, *mentors)
            return topic
        except (ValueError, IntegrityError):
            LOGGER.error('Inappropriate value or relational integrity fail')

    def update(self, title=None, description=None):
        """
        Method that updates topic object according to the accepted info.

        :param title: Title of the certain topic.
        :type title: string

        :param description: Describing topic
        :type description: string

        :return: None
        """

        if title:
            self.title = title
        if description:
            self.description = description

        self.save()

    def add_mentors(self, mentors_list):
        """Method that add mentors to topic"""

        if mentors_list:
            self.mentors.add(*mentors_list)

    def remove_mentors(self, mentors_list):
        """Method that remove mentors from topic"""

        if mentors_list:
            self.mentors.remove(*mentors_list)
