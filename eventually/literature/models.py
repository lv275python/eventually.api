"""
LiteratureItem model
=====================

This module implements class that represents the LiteratureItem model
"""
from django.db import models, IntegrityError
from authentication.models import CustomUser
from item.models import Item
from utils.utils import LOGGER


class LiteratureItem(models.Model):
    """
        Create LiteratureItem model

        Attributes:
        ===========

            :param title: title of literature item
            :type title: string

            :param description: description of literature item
            :type description: string

            :param source: source of literature item
            :type source: string

            :param author: id of author
            :type author: integer

            :param item: id of item
            :type item: integer

            :param create_at: The date when the certain event was created
            :type create_at: datetime

            :param update_at: The date when the certain event was last time edited
            :type update_at: datetime
    """

    title = models.CharField(max_length=100)
    description = models.CharField(blank=True, max_length=300)
    source = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, null=True)
    item = models.ForeignKey(Item, null=True)

    def __repr__(self):
        """
        Method that returns string representation of
        vote instance object.

        :return: literature_item id, title, description, source, author
        """
        return "id:{} title:{} description:{} source:{} author:{} item:{}".format(self.id,
                                                                                  self.title,
                                                                                  self.description,
                                                                                  self.source,
                                                                                  self.author.id,
                                                                                  self.item.id)

    def __str__(self):
        """
        Magic method that returns string representation of
        vote instance object.

        :return: literature_item id, title, description, source, author
        """
        return "id:{} title:{} description:{} source:{} author:{} item:{}".format(self.id,
                                                                                  self.title,
                                                                                  self.description,
                                                                                  self.source,
                                                                                  self.author.id,
                                                                                  self.item.id)

    def to_dict(self):
        """
        Method that return LiteratureItem object in dictionary

        :return:models-fields in dictionary

        :Example:
         | {
         |     'id': 13,
         |     'title':'Title of interesting book',
         |     'description': 'Description of interesting book',
         |     'source': 'book.com',
         |     'created_at': 1509540116,
         |     'updated_at': 1509540116,
         |     'author': 1,
         |     'item': 3,
         | }
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'source': self.source,
            'create_at': int(self.create_at.timestamp()),
            'update_at': int(self.update_at.timestamp()),
            'author': self.author.id,
            'item': self.item.id,
        }

    @staticmethod
    def get_by_id(literature_id):
        """
        Static method that return LiteratureItem object by id

        :param literature_id: id of element in model
        :type literature_id: integer

        :return: object with element, searched by id
        """
        try:
            return LiteratureItem.objects.get(id=literature_id)
        except LiteratureItem.DoesNotExist:
            LOGGER.error(f'The literature with id={literature_id} does not exist')

    @staticmethod
    def create(title, source, author, item, description=""):
        """
        Static method that create new LiteratureItem object

        :param title: title of literature item
        :type title: string

        :param description: description of literature item
        :type description: string

        :param source: source of literature item
        :type source: string

        :param author: id of author
        :type author: integer

        :param item: id of item
        :type item: integer

        :return: new created object or None
        """
        literature = LiteratureItem(title=title,
                                    description=description,
                                    source=source,
                                    author=author,
                                    item=item)
        try:
            literature.save()
            return literature
        except (ValueError, IntegrityError):
            LOGGER.error('Value or integrity error error was raised')

    def update(self, title="", description="", source=""):
        """
        Method that update existed LiteratureItem object

        :param title: title of literature item
        :type title: string

        :param description: description of literature item
        :type description: string

        :param source: source of literature item
        :type source: string

        :return: updated object or none
        """

        if title:
            self.title = title
        if description:
            self.description = description
        if source:
            self.source = source

        self.save()

    @staticmethod
    def delete_by_id(literature_id):
        """
        Method delete existed LiteratureItem object by id

        :param literature_id: id of object
        :type literature_id: integer

        :return:deleted LiteratureItem object
        """
        try:
            literature = LiteratureItem.objects.get(id=literature_id)
            literature.delete()
            return True
        except (LiteratureItem.DoesNotExist, AttributeError):
            LOGGER.error(f'The literature with id={literature_id} was not deleted')
