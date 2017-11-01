"""
Vote & Answer models
====================

This module implements class that represents the vote and answer models
"""
from django.db import models, IntegrityError


class Vote(models.Model):
    """
        ..class::Vote

        Create Vote model

        Attributes:
        ===========

            :param is_active: active vote or end
            :type is_active: BooleanField

            :param is_extended:
            :type is_extended: BooleanField

            :param title: title of vote
            :type title: CharField

            :param vote_type: type of vote - we can choose one answer or many
            :type vote_type: CharField

            :param create_at:
            :type create_at: TimeField

            :param update_at:
            :type update_at: TimeField
    """

    MULTI_CHOICES = (
        ('O', 'One'),
        ('M', 'Multi'),
    )

    is_active = models.BooleanField(default=True)
    is_extended = models.BooleanField(default=True)
    title = models.TextField(max_length=100)
    vote_type = models.CharField(max_length=2, choices=MULTI_CHOICES)
    create_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        """
        Method that return Vote object in dictionary

        :return:models-fields in dictionary

        :Example:
         {
             'id': 13,
             'is_active': True,
             'is_extended': True,
             'title': 'Title of vote',
             'type': 'M',
             'created_at': 1509540116,
             'updated_at': 1509540116,
         }
        """
        return {
            'id':self.id,
            'is_active': self.is_active,
            'is_extended': self.is_extended,
            'title': self.title,
            'type': self.vote_type,
            'create_at': int(self.create_at.timestamp()),
            'update_at': int(self.update_at.timestamp()),
        }

    @staticmethod
    def get_by_id(vote_id):
        """
        Static method that return Vote object by id

        :param vote_id: id of element in model
        :type id: IntegerField

        :return: object with element, searched by id
        """
        try:
            return Vote.objects.get(id=vote_id)
        except Vote.DoesNotExist:
            pass

    @staticmethod
    def create(is_active=True, is_extended=True, title="", vote_type='O'):
        """
        Static method that create new Vote object

        :param is_active: active vote or end
        :type is_active:BooleanField

        :param is_extended:
        :type is_extended: BooleanField

        :param title: title of vote
        :type title: CharField

        :param vote_type: type of vote - we can choose one answer or many
        :type title: CharField

        :return: new created object or None
        """
        vote = Vote(is_active=is_active,
                    is_extended=is_extended,
                    title=title,
                    vote_type=vote_type)

        try:
            vote.save()
            return vote
        except (ValueError, IntegrityError):
            pass

    def update(self, is_active=None, is_extended=None, title=None, vote_type=None):
        """
        Method that update existed Vote object

        :param is_active: active vote or end
        :type is_active: BooleanField

        :param is_extended:
        :type is_extended: BooleanField

        :param title: title of vote
        :type title: CharField

        :param vote_type: type of vote - we can choose one answer or many
        :type vote_type: CharField

        :return: none
        """
        if is_active:
            self.is_active = is_active
        if is_extended:
            self.is_extended = is_extended
        if title:
            self.title = title
        if vote_type:
            self.vote_type = vote_type

        self.save()

    @staticmethod
    def delete_by_id(vote_id):
        """
        Method delete existed Vote object by id

        :param vote_id: id of object
        :type vote_id: IntegerField

        :return:deleted Vote object
        """
        try:
            vote = Vote.objects.get(id=vote_id)
            vote.delete()
            return True
        except (Vote.DoesNotExist, AttributeError):
            pass


class Answer(models.Model):
    """
        ..class::Answer

        Create Answer model, that has variants to choose in Vote

        Attributes:
        ===========

        :param vote: foreign key of vote
        :type vote: ForeignKey

        :param text: variant to choose in vote
        :type text: TextField

        :param create_at:
        :type create_at: TimeField

        :param update_at:
        :type update_at: TimeField
    """
    vote = models.ForeignKey(Vote)
    text = models.TextField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        """
        Method that return Answer object in dictionary

        :return:models-fields in dictionary

        :Example:
         {
             'id': 12,
             'vote': 13,
             'text': 'My text',
             'created_at': 1509540116,
             'updated_at': 1509540116,
         }
        """
        return {
            'id': self.id,
            'vote': self.vote,
            'text': self.text,
            'create_at': self.create_at,
            'update_at': self.update_at
        }

    @staticmethod
    def get_by_id(answer_id):
        """
        Static method that return Answer object by id

        :param answer_id: id of element in model
        :type answer_id: IntegerField

        :return: object with element, searched by id
        """
        try:
            return Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            pass

    @staticmethod
    def create(my_vote=None, my_text=''):
        """
        Static method that create new Answer object

        :param my_vote: foreign key of vote
        :type my_vote: IntegerField

        :param my_text: variant to choose in vote
        :type my_text: CharField

        :return: new created object or None
        """
        answer = Answer(vote=my_vote,
                        text=my_text)

        try:
            answer.save()
            return answer
        except (ValueError, IntegrityError):
            pass

    def update(self, vote=None, text=None):
        """
        Method that update existed Answer object

        :param vote: foreign key of vote
        :type vote: IntegerField

        :param text: variant to choose in vote
        :type text: CharField

        :return: none
        """
        if vote:
            self.vote = vote
        if text:
            self.text = text
        self.save()

    @staticmethod
    def delete_by_id(answer_id):
        """
        Method delete existed Answer object by id

        :return:deleted Answer object
        """
        try:
            answer = Answer.objects.get(id=answer_id)
            answer.delete()
            return True

        except (Answer.DoesNotExist, AttributeError):
            pass
