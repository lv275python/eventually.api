"""
Task module.
==============

This module implements class that represents the task entity.
"""
from django.db import models, IntegrityError
from event.models import Event
from authentication.models import CustomUser


class Task(models.Model):
    """
     Describing of task entity.

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

            :param event: Foreign key on the certain Event model
            :type event: integer

            :param users: Foreign key on the certain CustomUser model
            :type users: integer
        """

    STATUS_TYPE_CHOICES = (
        (0, 'ToDo'),
        (1, 'In Progress'),
        (2, 'Done')
    )

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    status = models.IntegerField(default=0, choices=STATUS_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    users = models.ManyToManyField(CustomUser)

    def __repr__(self):
        """
        Magic method that returns representation of
        task instance object.

        :return: task title, task description, task status, created , updated, event id, users id
        """

        return f'{self.__class__.__name__}(id={self.id})'

    def __str__(self):
        """
        Magic method that returns string representation of
        task instance object.

        :return: task title, task description, task status, created , updated, event id, users id
        """

        return str(self.to_dict())[1:-1]

    def to_dict(self):
        """
        Method that converts task object to dictionary.

        :return: dictionary with task's information

        :Example:

        | {
        |    'id': 17,
        |    'title': 'My awesome title',
        |    'description': 'My awesome description',
        |    'status': 1,
        |    'created_at': 1509540116,
        |    'updated_at': 1509540116,
        |    'event' : 13,
        |    'users' : [21, 33]
        | }
        """

        return {'id': self.id,
                'title': self.title,
                'description': self.description,
                'status': self.status,
                'created_at': int(self.created_at.timestamp()),
                'updated_at': int(self.updated_at.timestamp()),
                'event': self.event.id,
                'users': [user.id for user in self.users.all()]}

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
    def create(event, users=None, title=None, description=None, status=0):
        """
        Static method that creates instance of Task class and creates database
        row with the accepted info.

        :param: event: Certain Event's object. Is required.
        :type event: Event model.

        :param: users: Certain tuple CustomUser's objects. Is required.
        :type tuple<users>: CustomUser model.

        :param title: Title of the certain task.
        :type title: string

        :param description: Describing goals for successful event performance
        :type description: string

        :param status: Stage of the task.
        :type status: integer

        :return: task object or None if task have not created
        """

        task = Task()
        task.event = event
        task.title = title
        task.description = description
        task.status = status

        try:
            task.save()
            task.users.add(*users)
            return task
        except (ValueError, IntegrityError):
            pass

    def update(self, title=None, description=None, status=None):
        """
        Method that updates task object according to the accepted info.

        :param: event: Certain Event's object.
        :type event: Event model.

        :param: users: Certain tuple CustomUser's objects.
        :type <tuple>users: CustomUser model.

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


    def add_users(self, users_list):
        """Method that add users to task"""

        if users_list:
            self.users.add(*users_list)


    def remove_users(self, users_list):
        """Method that remove users from task"""

        if users_list:
            self.users.remove(*users_list)
