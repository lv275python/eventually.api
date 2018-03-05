"""
LiteratureItem model
=====================

This module implements class that represents the LiteratureItem model
"""
# pylint: disable=arguments-differ

from django.db import models, IntegrityError
from authentication.models import CustomUser
from item.models import Item
from utils.abstractmodel import AbstractModel
from utils.utils import LOGGER


class LiteratureItem(AbstractModel):
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
    author = models.ForeignKey(CustomUser)
    item = models.ForeignKey(Item, null=True)


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
