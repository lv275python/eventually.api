"""
Model for describe Comment entity
"""
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.dateformat import format

# Create your models here.

class Comment(models.Model):
    """
        Comment model that describes comment entity.

        The main idea is to document
        the class with

        :param text: text of comment using CharField with max_length = 1024 symbols
        :param created_at: date of comment's create using datetime format
        :param updated_at: date of comment's update using datetime format

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

    def get_created_at(self):
        """
        This is a method to show date in Unix date format.

        :return: date in Unix date format

        """
        date = format(self.created_at, u'U')

        return date

    def to_dict(self):
        """
        Return dictionary with comment's info

        :return: dictionary with comment's info

        """

        return {'id': self.id,
                'text': self.text,
                'created_at': self.created_at,
                'updated_at': self.updated_at
               }

    @staticmethod
    def get_by_id(comment_id):
        """
        Return comment, found by id.

        :param comment_id: comment's id
        :return: Comment object instance or None if object does not exist

        """
        try:
            comment = Comment.objects.get(id=comment_id)
            return comment
        except Comment.DoesNotExist:
            return None

    @staticmethod
    def create(text='simple comment'):
        """
        Create comment.

        :param text: - text of comment
        :return: Comment object instance

        """
        comment = Comment.objects.create(text=text)
        comment.save()
        return comment

    def update(self, text=None):
        """
        Update comment's text.

        :param text: - text of comment

        """
        if text:
            self.text = text

        self.save()

    @staticmethod
    def delete_by_id(comment_id):
        """
        Delete comment, found by id.

        :param comment_id: - comment's id
        :return: True if comment seccessfully deleted or None if object does not exist

        """
        try:
            comment = Comment.objects.get(id=comment_id).delete()
            return True
        except Comment.DoesNotExist:
            return None
