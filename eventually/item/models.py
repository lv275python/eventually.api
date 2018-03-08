"""
Item model
==========

This module implements class that represents the item entity.
"""
# pylint: disable=arguments-differ

from django.db import models, IntegrityError
from authentication.models import CustomUser
from topic.models import Topic
from utils.abstractmodel import AbstractModel
from utils.utils import LOGGER


class Item(AbstractModel):
    """
    Describing of item entity.

    Attributes:
    ===========

        :param name: Name of the certain item.
        :type name: str

        :param authors: List of the authors of certain item instance.
                        Reference to the CustomUser model.
        :type authors: list

        :param form: The type of the certain item that define the item requirements.
        :type form: int

        :param topic: The topic that contains the current item. Reference to the Topic model.
        :type topic: list

        :param superiors: List of other items that have to be done for the possibility to start
                          work on the current item.
        :type superiors: list

        :param description: Describing core requirements and goals of the item.
        :type description: str

        :param estimation: The recommended time for passing the current item.
        :type estimation: timedelta

        :param created_at: The date when the certain item was created.
        :type: created_at: datetime

        :param updated_at: The date when the certain item was last time edited.
        :type updated_at: datetime
    """

    ITEM_FORMS = ((0, 'theoretic'),
                  (1, 'practice'),
                  (2, 'group'))

    name = models.CharField(max_length=255)
    authors = models.ManyToManyField(CustomUser)
    topic = models.ForeignKey(Topic)
    form = models.IntegerField(choices=ITEM_FORMS)
    superiors = models.ManyToManyField('self', related_name='subordinates', symmetrical=False)
    description = models.TextField(blank=True)
    estimation = models.DurationField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        """
        Method that converts item object to dictionary.

        :return: dictionary with item's information
        :rtype dict

        :Example:

        | {'id': 4,
        |  'name': 'read,
        |  'authors': [12],
        |  'topic': 23,
        |  'form': 2,
        |  'superiors': [2, 4, 12]
        |  'description': 'description',
        |  'estimation': 54000,
        |  'created_at': 1509539867,
        |  'updated_at': 1509539867}
        """

        return {'id': self.id,
                'name': self.name,
                'authors': sorted([author.id for author in self.authors.all()]),
                'topic': self.topic.id,
                'form': self.form,
                'superiors': sorted([superior.id for superior in self.superiors.all()]),
                'description': self.description,
                'estimation': int(self.estimation.total_seconds()) if self.estimation else None,
                'created_at': int(self.created_at.timestamp()),
                'updated_at': int(self.updated_at.timestamp())}

    @staticmethod
    def create(topic, authors, name, form, superiors=None, description='', estimation=None):
        """
        Static method that creates instance of Item class and creates database
        row with the accepted info.

        :param name: Name of the certain item.
        :type name: str

        :param authors: List of authors the certain item.
        :type authors: list

        :param form: The type of the certain item that define the item requirements.
        :type form: int

        :param topic: The Topic object that the current item belongs to.
        :type  topic: int

        :param superiors: List of other items that have to be done for the possibility to start
                          work on the current item.
        :type superiors: list

        :param description: Describing core requirements and goals of the item.
        :type description: str

        :param estimation: The recommended time for passing the current item.
        :type estimation: timedelta

        :return: item object or None if event have not created
        """

        item = Item()
        item.name = name
        item.form = form
        item.topic = topic
        item.description = description
        item.estimation = estimation
        try:
            item.save()
            item.authors.add(*authors)
            item.superiors.add(*superiors)
            return item
        except (ValueError, IntegrityError):
            LOGGER.error('Inappropriate value or relational integrity fail')

    def update(self, name=None, form=None, description=None, estimation=None):
        """
        Method that updates the certain instance of Item class accordingly
        to the accepted parameters.

        :param name: Name of the certain item.
        :type name: str

        :param form: The type of the certain item that define the item requirements.
        :type form: int

        :param description: Describing core requirements and goals of the item.
        :type description: str

        :param estimation: The recommended time for passing the current item.
        :type estimation: timedelta

        :return: None
        """

        if name:
            self.name = name
        if form:
            self.form = form
        if description:
            self.description = description
        if estimation:
            self.estimation = estimation

    def update_authors(self, authors_add=None, authors_del=None):
        """
        Method that updates the authors field of the certain instance of Item class accordingly
        to the accepted parameters.

        :param authors_add: the list of CustomUser model items that have to be added like authors.
        :type authors_add: list

        :param authors_del: the list of CustomUser model items that have to be removed from authors.
        :type authors_del: list

        :return: None
        """

        if authors_add:
            self.authors.add(*authors_add)
        if authors_del:
            self.authors.remove(*authors_del)

    def update_superiors(self, superiors_add=None, superiors_del=None):
        """
        Method that updates the superiors field of the certain instance of Item class accordingly
        to the accepted parameters.

        :param superiors_add: the list of Item model items that have to be added like superiors.
        :type superiors_add: list

        :param superiors_del: the list of Item model items that have to be removed from superiors.
        :type superiors_del: list

        :return: None
        """

        if superiors_add:
            self.superiors.add(*superiors_add)
        if superiors_del:
            self.superiors.remove(*superiors_del)
