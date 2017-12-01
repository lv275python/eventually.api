"""
Assignment model
=======================

This module implements class that represents the assignment entity.
"""
from django.db import models, IntegrityError
from authentication.models import CustomUser
# from item.models import Item



class Assignment(models.Model):

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
    statement = models.CharField(max_length=1024, blank=True)
    grade = models.FloatField(null=True)
    user = models.ForeignKey(CustomUser, null=True)
    # item = models.ForeignKey(Item, null=True)
    status = models.IntegerField(default=0, choices=STATUS_TYPE_CHOICES)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Magic method that returns string representation of
        assignment instance object.

        :return: string with assignment's information
        """

        return "{} {} {} {} {} {} {}".format(self.id,
                                             self.statement,
                                             self.grade,
                                             self.user.id if self.user else None,
                                             # self.item.id if self.item else None,
                                             self.status,
                                             self.started_at,
                                             self.finished_at,)

    def __repr__(self):
        """
        Magic method that returns representation of
        assignment instance object.

        :return: string with assignment's information
        """

        return "{} {} {} {} {}".format(self.id,
                                       self.statement,
                                       self.grade,
                                       self.status,
                                       self.user.id if self.user else None,)
                                       # self.item.id if self.item else None,)

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
                # 'item_id': self.assignment.id if self.assignment else None,
                'status': self.status,
                'started_at': int(self.created_at.timestamp()),
                'finished_at': int(self.updated_at.timestamp()),
                'created_at': int(self.created_at.timestamp()),
                'updated_at': int(self.updated_at.timestamp())}

    @staticmethod
    def get_by_id(assignment_id):
        """
        Static method that returns assignment objects according to the accepted id.
        Return comment, found by id.

        :param assignment_id: assignment's id
        :type assignment_id: int

        :return: Assignment object instance or None if object does not exist
        """

        try:
            return Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist:
            pass

    @staticmethod
    def create(statement,
               grade,
               user=None,
               # item=None,
               status=0,
               started_at=None,
               finished_at=None):
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
        assignment.statement = statement
        assignment.grade = grade
        assignment.user = user
        # assignment.item = item
        assignment.status = status
        assignment.started_at = started_at
        assignment.finished_at = finished_at
        try:
            assignment.save()
            return assignment
        except (ValueError, IntegrityError):
            pass

    def update(self,
               statement=None,
               grade=None,
               user=None,
               # item=None,
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
         # if item:
         #     self.item = item
        if status:
            self.status = status
        if started_at:
            self.started_at = started_at
        if finished_at:
            self.finished_at = finished_at
        self.save()

    @staticmethod
    def delete_by_id(assignment_id):
        """
        Static method that removes Assignment object according to the accepted id.

        :param assignment_id: assignment's id
        :type assignment_id: int

        :return: True if object succseffull deleted or
                            None if object isnt found
        """
        try:
            assignment = Assignment.objects.get(id=assignment_id)
            assignment.delete()
            return True
        except (Assignment.DoesNotExist, AttributeError):
            pass
