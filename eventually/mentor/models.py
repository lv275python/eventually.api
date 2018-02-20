"""
MentorStudent model
===================

This module implements class that represents the relation between students
and mentors and theirs topics.
"""

# pylint: disable=arguments-differ

from django.db import models, IntegrityError
from utils.abstractmodel import AbstractModel
from utils.utils import LOGGER
from authentication.models import CustomUser
from topic.models import Topic


class MentorStudent(AbstractModel):
    """
    Describing of relation between mentor and student.

    :param mentor: the certain CustomUser model instance.
    :type mentor: int

    :param student: the certain CustomUser model instance.
    :type student: int

    :param topic: the certain Topic model instance.
    :type topic: int

    :param is_done: the status of a student passing a particular topic.
    :type is_done: bool

    :param create_at: The date when the certain record was created
    :type create_at: datetime

    :param update_at: The date when the certain record was last time edited
    :type update_at: datetime
    """

    mentor = models.ForeignKey(CustomUser, null=True, related_name='mentor')
    student = models.ForeignKey(CustomUser, related_name='student')
    topic = models.ForeignKey(Topic)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        """
        Method that converts MentorStudent object to dictionary.

        :return: dictionary with MentorStudent's information

        :Example:

        | {
        |    'id': 4,
        |    'mentor:' 12,
        |    'student': 3,
        |    'is_done: True,
        |    'created_at': 1509539867,
        |    'updated_at': 1509539867,
        | }
        """

        return {
            'id': self.id,
            'mentor': self.mentor.id if self.mentor else None,
            'student': self.student.id,
            'topic': self.topic.id,
            'is_done': self.is_done,
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp())
        }

    @staticmethod
    def create(student, topic, mentor=None, is_done=False):
        """mentor=None,
        Static method that creates instance of MentorStudent class and creates database
        record with the accepted info.

        :param mentor: Certain CustomUser's object. Is required.
        :type mentor: CustomUser model

        :param student: Certain CustomUser's object. Is required.
        :type student: CustomUser model

        :param topic: Certain Topic's object. Is required.
        :type topic: Topic model

        :param is_done: the status of a student passing a particular topic.
        :type is_done: bool

        :return: MentorStudent object or None if MentorStudent have not created
        """

        record = MentorStudent()
        record.mentor = mentor
        record.student = student
        record.topic = topic
        record.is_done = is_done
        try:
            record.save()
            return record
        except (ValueError, IntegrityError):
            LOGGER.error('Inappropriate value or relational integrity fail')

    def update(self, mentor=None, student=None, topic=None, is_done=None):
        """
        Method that updates the certain MentorStudent object according to the accepted info.

        :param mentor: Certain CustomUser's object. Is required.
        :type mentor: CustomUser model

        :param student: Certain CustomUser's object. Is required.
        :type student: CustomUser model

        :param topic: Certain Topic's object. Is required.
        :type topic: Topic model

        :param is_done: the status of a student passing a particular topic.
        :type is_done: bool

        :return: MentorStudent object or None if MentorStudent has not created
        """

        if mentor:
            self.mentor = mentor
        if student:
            self.student = student
        if topic:
            self.topic = topic
        if is_done:
            self.is_done = is_done
        self.save()

    @staticmethod
    def get_all():
        """
        returns data for json request with querysets of all MentorStudent objects
        """
        all_mentees = MentorStudent.objects.all()
        return all_mentees

    @staticmethod
    def get_my_students(mentor_id):
        """
        A method that get students who belong to a certain mentor

        :param mentor_id: Certain mentor id
        :type mentor_id: int

        :return: QuerySet with students
        """

        return MentorStudent.objects.filter(mentor_id=mentor_id)

    @staticmethod
    def get_my_mentors(student_id):
        """
        A method that get mentors who belong to a certain student

        :param student_id: Certain student id
        :type student_id: int

        :return: QuerySet with mentors
        """

        return MentorStudent.objects.filter(student_id=student_id)

    @staticmethod
    def get_assigned_students(mentor_id):
        """
        A method that only get students who signed in courses in which mentor can be certain mentor,
        but them mentor is not certain mentor

        :param mentor_id: Certain mentor id
        :type mentor_id: int

        :return: QuerySet with students
        """

        assigned_students = MentorStudent.objects.exclude(mentor_id=mentor_id)
        return assigned_students.exclude(mentor_id=None)

    @staticmethod
    def get_available_students():
        """
        A method that only get students who signed in courses in which mentor can be certain mentor,
        but they do not have a mentor yet

        :return: QuerySet with students
        """

        return MentorStudent.objects.filter(mentor_id=None)

    @staticmethod
    def get_topic_all_students(topic_id):
        """
        A method that only get students who signed in certain course.

        :return: QuerySet with students
        """
        return MentorStudent.objects.filter(topic_id=topic_id)

    @staticmethod
    def topic_student_belonging(topic_id, student_id):
        """
        A method that return MentorStudent instance if student assigned to course
        or None, if not.

        :return: MentorStudent instance
        """
        record = list(MentorStudent.objects.filter(topic_id=topic_id, student_id=student_id))
        if record:
            return record[0]
        return None
