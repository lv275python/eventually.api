"""
Comment Model Test.

This module provides complete testing for all Comment's model functions.
"""
import datetime
from unittest import mock
from django.test import TestCase
from django.utils import timezone
from authentication.models import CustomUser
from comment.models import Comment
from team.models import Team

TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12, 0, tzinfo=timezone.utc)


class CommentModelTestCase(TestCase):
    """TestCase for providing Comment model testing."""

    def setUp(self):
        """Provide preparation before testing Comment model's features."""
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME
            custom_user = CustomUser(id=2000,
                                     email='email.customuser@test.test')
            custom_user.set_password('123456')
            custom_user.save()

            receiver = CustomUser(id=1500,
                                  email='email.receiver@test.test')
            receiver.set_password("123456789")
            receiver.save()

            team = Team(id=1000,
                        owner=custom_user,
                        members=[custom_user],
                        name='barcelona')
            team.save()

            comment = Comment(id=100,
                              team=team,
                              author=custom_user,
                              text='football',
                              receiver=receiver)
            comment.save()

            comment = Comment(id=200,
                              team=team,
                              author=custom_user,
                              text='tennis',
                              receiver=receiver
                              )
            comment.save()

    def test_str(self):
        """Method that tests `__str__` method of certain Comment instance."""
        comment = Comment.objects.get(id=100)
        expected_comment_str = "'id': 100, " \
                               "'text': 'football', " \
                               "'created_at': 1509351312, " \
                               "'updated_at': 1509351312, " \
                               "'team': 1000, " \
                               "'event': None, "\
                               "'task': None, " \
                               "'vote': None, " \
                               "'author': 2000, " \
                               "'receiver': 1500"

        self.assertEqual(comment.__str__(), expected_comment_str)

    def test_repr(self):
        """Method that tests `__repr__` method of certain Comment instance."""
        comment = Comment.objects.get(id=100)
        expected_comment_repr = "Comment(id=100)"

        self.assertEqual(repr(comment), expected_comment_repr)

    def test_to_dict(self):
        """Method that tests `to_dict` method of certain Comment instance."""
        comment = Comment.objects.get(id=100)
        expected_comment_dict = {
            "id": 100,
            "text": "football",
            "created_at": 1509351312,
            "updated_at": 1509351312,
            "team": 1000,
            "event": None,
            "task": None,
            "vote": None,
            "author": 2000,
            "receiver": 1500
        }

        comment_dict = comment.to_dict()

        self.assertDictEqual(comment_dict, expected_comment_dict)

    def test_success_get_by_id(self):
        """Method that tests `get_by_id` method of Comment class object."""
        actuall_comment = Comment.get_by_id(100)
        expected_comment = Comment.objects.get(id=100)

        self.assertEqual(actuall_comment, expected_comment)

    def test_fail_get_by_id(self):
        """Method that tests `get_by_id` method of Comment class object."""
        comment = Comment.get_by_id(185)

        self.assertIsNone(comment)

    def test_seccess_create(self):
        """Method that tests `create` method of Comment class object."""
        team = Team.objects.get(id=1000)
        author = CustomUser.objects.get(id=2000)
        text = "hello"
        comment = Comment.create(team=team, author=author, text=text)
        self.assertIsInstance(comment, Comment)
        self.assertEqual(comment.team, team)
        self.assertEqual(comment.author, author)
        self.assertEqual(comment.text, text)
        self.assertIsNone(comment.event)
        self.assertIsNone(comment.task)
        self.assertIsNone(comment.vote)

    def test_fail_create(self):
        """Method that tests `create` method of Comment class object."""
        team = Team()
        author = CustomUser.objects.get(id=2000)
        comment = Comment.create(team=team, author=author)

        self.assertIsNone(comment)

    def test_update(self):
        """Method that tests `update` method of certain Comment instance."""
        comment = Comment.objects.get(id=100)

        new_text = 'Hello world'
        comment.update(text=new_text)

        expected_comment = Comment.objects.get(id=100)

        self.assertEqual(comment.text, new_text)
        self.assertEqual(comment, expected_comment)

    def test_seccess_delete_by_id(self):
        """Method that tests `delete_by_id` method of Comment class object."""
        self.assertTrue(Comment.delete_by_id(100))
        self.assertRaises(Comment.DoesNotExist, Comment.objects.get, id=100)

    def test_fail_delete_by_id(self):
        """Method that tests `delete_by_id` method of Comment class object."""
        self.assertFalse(Comment.delete_by_id(300))
