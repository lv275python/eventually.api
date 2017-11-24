"""
Assignment answer model
=======================

This module implements class that represents the assignment_answer entity.
"""
from django.db import models, IntegrityError
from authentication.models import CustomUser
from team.models import Team
# from assignment.models import Assignment



class AssignmentAnswer(models.Model):

    """
    Describing of assignment_answer entity.
    Attributes:
    ===========

        :param statement: statement of the certain answer.
        :type statement: string

        :param grade: grade of the certain answer.
        :type grade: float

        :param create_date: The date when the certain answer was created.
        :type: create_date: datetime

        :param update_date: The date when the certain answer was last time edited.
        :type: create_date: datetime

        :param user: Describing relation between user's answer and user.
        :type user: int

        :param team: Describing relation between team's answer and team.
        :type team: int

        :param assignment: Describing relation between answer and assignment.
        :type assignment: int
    """
    statement = models.CharField(max_length=1024, blank=True)
    grade = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, null=True)
    team = models.ForeignKey(Team, null=True)
#   assignment = models.ForeignKey(Assignment, null=True)

    def __str__(self):
        """
        Magic method that returns string representation of
        assignment_answer instance object.

        :return: string with assignment_answer's information
        """

        return "{} {} {} {} {} {} {} {}".format(self.id,
                                                self.statement,
                                                self.grade,
                                                self.created_at,
                                                self.updated_at,
                                                self.user.id if self.user else None,
                                                self.team.id if self.team else None,
                                                self.assignment.id if self.assignment else None,)

    def __repr__(self):
        """
        Magic method that returns representation of
        assignment_answer instance object.

        :return: string with assignment_answer's information
        """

        return "{} {} {} {} {} {}".format(self.id,
                                          self.statement,
                                          self.grade,
                                          self.user.id if self.user else None,
                                          self.team.id if self.team else None,
                                          self.assignment.id if self.assignment else None,)

    def to_dict(self):
        """
        Method that converts assignment_answer object to dictionary.

        :return: dictionary with assignment_answer's information

        :Example:
            | {
            |   'id': 1,
            |   'statement': 'name',
            |   'grade': 'img',
            |   'created_at': 1509539536196,
            |   'updated_at': 1509539536196,
            |   'user_id': 2,
            |   'team_id': 3,
            |   'assignment_id': 3
            | }
        """

        return {'id': self.id,
                'statement': self.statement,
                'grade': self.grade,
                'created_at': int(self.created_at.timestamp()),
                'updated_at': int(self.updated_at.timestamp()),
                'user_id': self.user.id if self.user else None,
                'team_id': self.team.id if self.team else None,
                'assignment_id': self.assignment.id if self.assignment else None}

    @staticmethod
    def get_by_id(assignment_answer_id):
        """
        Static method that returns assignment_answer objects according to the accepted id.
        Return comment, found by id.

        :param assignment_answer_id: team's id
        :type assignment_answer_id: int

        :return: AssignmentAnswer object instance or None if object does not exist
        """

        try:
            return AssignmentAnswer.objects.get(id=assignment_answer_id)
        except AssignmentAnswer.DoesNotExist:
            pass

    @staticmethod
    def create(statement, grade, user=None, team=None):
        """
        Static method that creates instance of AssignmentAnswer class and creates databes
        row with the accepted info.

        :param statement: assignment_answer's statement
        :type statement: str

        :param grade: assignment_answer's grade
        :type grade: float

        :param assignment: assignment that assignment_answer is related to
        :type assignment: Assignment obj

        :param user: user that assignment_answer is related to
        :type user: CustomUser obj

        :param team: team that assignment_answer is related to
        :type team: Team obj

        :return: AssignmentAnswer object instance or None if object does not exist
        """

        assignment_answer = AssignmentAnswer()
        assignment_answer.statement = statement
        assignment_answer.grade = grade
        assignment_answer.user = user
        assignment_answer.team = team
        try:
            assignment_answer.save()
            return assignment_answer
        except (ValueError, IntegrityError):
            pass

    def update(self, statement=None, grade=None, user=None, team=None):
        """
        Method that updates AssignmentAnswer object according to the accepted info.

        :param statement: assignment_answer's statement
        :type statement: str

        :param grade: assignment_answer's grade
        :type grade: float

        :param assignment: assignment that assignment_answer is related to
        :type assignment: Assignment obj

        :param user: user that assignment_answer is related to
        :type user: CustomUser obj

        :param team: team that assignment_answer is related to
        :type team: Team obj

        :return: None
        """
        if statement:
            self.statement = statement
        if grade:
            self.grade = grade
        if user:
            self.user = user
        if team:
            self.team = team
        self.save()

    @staticmethod
    def delete_by_id(assignment_answer_id):
        """
        Static method that removes AssignmentAnswer object according to the accepted id.

        :param assignment_answer_id: assignment_answer's id
        :type assignment_answer_id: int

        :return: True if object succseffull deleted or
                            None if object isnt found
        """
        try:
            assignment_answer = AssignmentAnswer.objects.get(id=assignment_answer_id)
            assignment_answer.delete()
            return True
        except (AssignmentAnswer.DoesNotExist, AttributeError):
            pass
