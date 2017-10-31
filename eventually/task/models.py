"""
Task module.
==============

This module implements class that represents the task entity.
"""
from django.db import models


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

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.IntegerField(default=0, choices=STATUS_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Magic method that returns string representation of
        event instance object.

        :return: task title, task description, task status
        """

        return "{} {} {}".format(self.title, self.description, self.status)

    def to_dict(self):
        """
        Method that converts task object to dictionary.

        :return: dictionary with task's information
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
        Static method that returns task objects according to the accepted id.

        :param task_id: Unique identificator of task.
        :type task_id: integer

        :return: task object or None if task does not exist
        """

        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            pass

    @staticmethod
    def create(title=None, description=None, status=0):
        """
        Static method that creates instance of Task class and creates database
        row with the accepted info.

        :param title: Title of the certain task.
        :type title: string

        :param description: Describing goals for successful event performance
        :type description: string

        :param status: Stage of the task.
        :type status: integer

        :return: task object or None if task have not created
        """

        task = Task()
        task.title = title
        task.description = description
        task.status = status

        try:
            task.save()
            return task
        except ValueError:
            pass

    def update(self, title=None, description=None, status=None,):
        """
        Method that updates task object according to the accepted info.

        :param title: Title of the certain task.
        :type title: string

        :param description: Describing goals for successful event performance
        :type description: string

        :param status: Stage of the task.
        :type status: integer

        :return: None
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
        Static method that removes task object according to the accepted id.

        :param task_id: Unique identificator of task.
        :type task_id: integer

        :return: task object or None if task does not exist
        """
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return True
        except (Task.DoesNotExist, AttributeError):
            pass
