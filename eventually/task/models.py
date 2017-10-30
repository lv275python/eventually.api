"""
Task module.
==============

This module implements class that represents the task entity.
"""
from django.db import models
from django.db import IntegrityError


class Task(models.Model):
    """Task model.
        Describing of task .
        Attributes:
            :param title: Title of the certain task.
            :type tittle: string

            :param description: Describing goals for successful event performance
            :type description: string

            :param status: Stage of the task .
            :type status: integer

            :param created_at: The date when the
            certain task was created.
            :type created_at: datatime

            :param updated_at: The date when the certain
            task was last time edited.
            :type updeted_at: datatime
        """

    STATUS_TYPE_CHOICES = (
        (0, 'ToDo'),
        (1, 'In Progress'),
        (2, 'Done')
    )

    title = models.CharField(max_length=255, null=True)
    description = models.TextField()
    status = models.IntegerField(default=0, choices=STATUS_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        """
        :param:
        """

        return {
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @staticmethod
    def get_by_id(task_id):
        """
        :param
        """

        try:
            task = Task.objects.get(id=task_id)
            return task
        except DoesNotExist:
            return None

    @staticmethod
    def create(title=None, description=None, status=0):
        """
        :param
        """

        task = Task()
        task.title = title
        task.description = description
        task.status = status

        try:
            task.save()
            return task
        except IntegrityError:
            return None

    def update(self, title=None, description=None, status=None,):
        """
        :param
        """

        if title:
            self.title = title
        if description:
            self.description = description
        if status:
            self.status = status

        self.save()

    @staticmethod
    def delete_by_id(task_id):
        """
        :param
        """
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
        except Task.DoesNotExist:
            pass
