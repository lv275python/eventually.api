"""
Assignment model
=======================

This module implements class that represents the assignment entity.
"""
# pylint: disable=arguments-differ
import pickle
from django.db import models, IntegrityError
from django.conf import settings
from django.core.cache import cache
from authentication.models import CustomUser
from item.models import Item

from utils.abstractmodel import AbstractModel
from utils.topic_views_functions import find_mentors_topics
from utils.utils import LOGGER

from curriculum.models import Curriculum
from topic.models import Topic

CACHE_TTL = settings.CACHE_TTL

class Assignment(AbstractModel):

    """
    Describing of assignment entity.
    Attributes:
    ===========

        :param statement: statement of the certain assignment.
        :type statement: string

        :param grade: grade of the certain assignment.
        :type grade: float

        :param create_date: The date when the certain assignment was created.
        :type: create_date: datetime

        :param update_date: The date when the certain assignment was last time edited.
        :type: create_date: datetime

        :param user: Describing relation between user's assignment and user.
        :type user: int

        :param team: Describing relation between team's assignment and team.
        :type team: int

        :param item: Describing relation between assignment and item.
        :type item: int
    """
    STATUS_TYPE_CHOICES = (
        (0, 'requested'),
        (1, 'in_process'),
        (2, 'done')
    )

    statement = models.CharField(max_length=300, blank=True)
    grade = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, choices=STATUS_TYPE_CHOICES)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        """
        Method that converts assignment object to dictionary.

        :return: dictionary with assignment's information

        :Example:
            | {
            |   'id': 1,
            |   'statement': 'name',
            |   'grade': 'img',
            |   'user_id': 2,
            |   'item_id': 3,
            |   'status' : 2,
            |   'started_at': 1509539536196,
            |   'finished_at': 1509539536196,
            |   'created_at': 1509539536196,
            |   'updated_at': 1509539536196,
            | }
        """

        return {'id': self.id,
                'statement': self.statement,
                'grade': self.grade,
                'user_id': self.user.id if self.user else None,
                'item_id': self.item.id if self.item else None,
                'status': self.status,
                'started_at': int(self.started_at.timestamp()) if self.started_at else None,
                'finished_at': int(self.finished_at.timestamp()) if self.finished_at else None,
                'created_at': int(self.created_at.timestamp()),
                'updated_at': int(self.updated_at.timestamp())}



    @staticmethod
    def create(user, item):

        """
        Static method that creates instance of Assignment class and creates databes
        row with the accepted info.

        :param statement: assignment's statement
        :type statement: str

        :param grade: assignment's grade
        :type grade: float

        :param item: item that assignment is related to
        :type item: Item obj

        :param user: user that assignment is related to
        :type user: CustomUser obj

        :param status: The number that points to the certain stage of the assignment processing.
        :type status: int

        :param started_at: time when student started this assignment
        :type started_at: datetime

        :param finished_at: time when student finished this assignment
        :type finished_at: datetime

        :return: Assignment object instance or None if object does not exist
        """

        assignment = Assignment()
        assignment.user = user
        assignment.item = item

        try:
            assignment.save()
            return assignment
        except (ValueError, IntegrityError):
            LOGGER.error('Inappropriate value or relational integrity fail')


    def update(self,
               statement=None,
               grade=None,
               user=None,
               item=None,
               status=None,
               started_at=None,
               finished_at=None):
        """
        Method that updates Assignment object according to the accepted info.

        :param statement: assignment's statement
        :type statement: str

        :param grade: assignment's grade
        :type grade: float

        :param item: item that assignment is related to
        :type item: Item obj

        :param user: user that assignment is related to
        :type user: CustomUser obj

        :param status: The number that points to the certain stage of the assignment processing.
        :type status: int

        :param started_at: time when student started this assignment
        :type started_at: datetime

        :param finished_at: time when student finished this assignment
        :type finished_at: datetime

        :return: None
        """
        if statement:
            self.statement = statement
        if grade:
            self.grade = grade
        if user:
            self.user = user
        if item:
            self.item = item
        if status:
            self.status = status
        if started_at:
            self.started_at = started_at
        if finished_at:
            self.finished_at = finished_at
        self.save()

    @staticmethod
    def get_by_id(assignment_id):
        """
        returns object of Topic by id

        :param student_id: Certain student id
        :type student_id: int

        :return: QuerySet with assignments
        """
        redis_key = 'assignment_by_id_{0}'.format(assignment_id)
        if redis_key in cache:
            assignment = pickle.loads(cache.get(redis_key))
            return assignment
        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist:
            return None
        cached_topic = pickle.dumps(assignment)
        cache.set(redis_key, cached_topic, CACHE_TTL)
        return assignment

    @staticmethod
    def get_assignments_by_student_topic_item_ids(student_id, topic_id=None, item_id=None):
        """
        Method that gets assignments that belong to certain student
        :param student_id: Certain student id
        :type student_id: int

        :return: QuerySet with assignments
        """

        if item_id:
            assignments = Assignment.objects.get(user_id=student_id, item_id=item_id)
        elif topic_id:
            assignments = Assignment.objects.filter(user_id=student_id, item__topic_id=topic_id)
        else:
            assignments = Assignment.objects.filter(user_id=student_id)
        return assignments

    @staticmethod
    def get_curriculums(student_id):
        assignments = Assignment.objects.filter(user=student_id).exclude(status=2)
        curriculums_id = assignments.values_list('item__topic__curriculum', flat=True).distinct()
        curriculums = [Curriculum.get_by_id(id) for id in curriculums_id]
        return curriculums

    @staticmethod
    def get_topics(student_id, curriculum_id=None):
        if curriculum_id:
            assignments = Assignment.objects.filter(user=student_id,
                                                    item__topic__curriculum=curriculum_id).exclude(status=2)
            topic_ids = assignments.values_list('item__topic', flat=True).distinct()
            topics = [Topic.get_by_id(id) for id in topic_ids]
        else:
            assignments = Assignment.objects.filter(user=student_id).exlude(status=2)
            topic_ids = assignments.values_list('item__topic', flat=True).distinct()
            topics = [Topic.get_by_id(id) for id in topic_ids]
        return topics

    @staticmethod
    def get_assignments_by_mentor_id(mentor_id, topic_id=None):
        if topic_id:
            assignments = Assignment.objects.filter(user_id=mentor_id, item__topic_id=topic_id, item__form=1)
        else:
            assignments = Assignment.objects.filter(user_id=mentor_id, item__form=1)
        return assignments

    @staticmethod
    def get_curriculums_by_mentor_id(mentor_id):
        assigments = Assignment.objects.filter(item__form=1, item__topic__mentors__in = [mentor_id]).exclude(status=2)
        curriculums_id = assigments.values_list('item__topic__curriculum', flat=True).distinct()
        curriculums = [Curriculum.get_by_id(id) for id in curriculums_id]
        return curriculums

    @staticmethod
    def get_topics_by_mentor_id(mentor_id, curriculum_id=None):
        if curriculum_id:
            assignments = Assignment.objects.filter(user=mentor_id,
                                                    item__form=1,
                                                    item__topic__curriculum=curriculum_id).exclude(status=2)

            mentor_topic_ids = assignments.values_list('item__topic').distinct()
            topics = [Topic.get_by_id(id) for id in mentor_topic_ids]
        else:
            assignments = Assignment.objects.filter(item__form=1,user=mentor_id).exlude(status=2)
            mentor_topic_ids = assignments.values_list('item__topic').distinct()
            topics = [Topic.get_by_id(id) for id in mentor_topic_ids]
        return topics
