"""
Model for describe Comment entity
"""

from django.db import models
from django.db import IntegrityError


class Comment(models.Model):
    """
        Comment model that describes comment entity.

        The main idea is to document
        the class with

        :param text: text of comment
        :type text: string with max_length = 1024 symbols
        :param created_at: date of comment's create
        :type  reated_at: datetime
        :param updated_at: date of comment's update
        :type updated_at: datetime

    """

    text = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        This is a magic method to return string value of model's parametrs in
         understandible format.

        :return: id, text, create date, update date

        """

        return "{} {} {} {}".format(self.id,
                                    self.text,
                                    self.created_at,
                                    self.updated_at)


    def to_dict(self):
        """
        Return dictionary with comment's info

        :return: dictionary with comment's info
        :example:  {
                    'id': 1,
                    'text': 'simple commit',
                    'created_at': 1509540116,
                    'updated_at': 1509540116
                    }
        """

        return {'id': self.id,
                'text': self.text,
                'created_at': int(self.created_at.timestamp()),
                'updated_at': int(self.updated_at.timestamp())
               }

    @staticmethod
    def get_by_id(comment_id):
        """
        Return comment, found by id.

        :param comment_id: comment's id
        :type comment_id: integer

        :return: Comment object instance or None if object does not exist

        """
        try:
            comment = Comment.objects.get(id=comment_id)
            return comment
        except Comment.DoesNotExist:
            pass

    @staticmethod
    def create(text=None):
        """
        Create comment.

        :param text: - text of comment
        :type text: string

        :return: Comment object instance

        """
        comment = Comment()
        comment.text = text
        try:
            comment.save()
            return comment
        except (ValueError, IntegrityError):
            pass

    def update(self, text=None):
        """
        Update comment's text.

        :param text: - text of comment
        :type text: string

        """
        if text:
            self.text = text

        self.save()

    @staticmethod
    def delete_by_id(comment_id):
        """
        Delete comment, found by id.

        :param comment_id: - comment's id
        :type comment_id: integer

        :return: True if comment seccessfully deleted or None if object does not exist

        """
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return True
        except (Comment.DoesNotExist, AttributeError):
            pass
