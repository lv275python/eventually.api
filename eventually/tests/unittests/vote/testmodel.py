import datetime
from django.test import TestCase
from django.db import transaction, IntegrityError
from unittest import mock
from authentication.models import CustomUser
from event.models import Event
from team.models import Team
from vote.models import Vote
from vote.models import Answer

TEST_TIME = datetime.datetime(2017, 10, 15, 8, 15, 12)


class VoteTestCase(TestCase):
    """TestCase for Vote model"""

    def setUp(self):
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            user = CustomUser(id=111,
                              email="email2",
                              password="pass2",
                              first_name="firstname2",
                              middle_name="middle2",
                              last_name="last2")
            user.save()

            team = Team(id=111,
                        owner=user,
                        members=[user],
                        name='team1')
            team.save()

            event = Event(id=111,
                          team=team,
                          owner=user,
                          name='event1')
            event.save()

            vote = Vote(id=111,
                        event=event,
                        title="title",
                        vote_type=0)
            vote.save()

            vote = Vote(id=222,
                        event=event,
                        is_active=True,
                        is_extended=False,
                        title="vote",
                        vote_type=1)
            vote.save()

    def test_vote_parameters_to_dict(self):
        """Method that tests `to_dict` method of certain Vote instance."""
        vote = Vote.objects.get(id=222)
        expect_vote_dict = {'id': 222,
                            'event': 111,
                            'is_active': True,
                            'is_extended': False,
                            'title': 'vote',
                            'vote_type': 1,
                            'create_at': 1508044512,
                            'update_at': 1508044512,
                            }
        actual_vote_dict = vote.to_dict()
        self.assertDictEqual(actual_vote_dict, expect_vote_dict)

    def test_vote_none_get_by_id(self):
        """Method that tests `to_dict` method of certain Vote instance."""
        vote = Vote.get_by_id(113)
        self.assertIsNone(vote)

    def test_vote_get_by_id(self):
        """Method that tests `to_dict` method of certain Vote instance."""
        vote = Vote.get_by_id(111)
        self.assertEqual(vote.id, 111)

    def test_vote_repr(self):
        """Method that test `__repr__` method of Vote instance object."""
        vote = Vote.objects.get(id=111)

        actual_repr = vote.__repr__()
        expected_repr = 'id:111 event:111 is_active:True is_extended:True title:title vote_type:0'
        self.assertEqual(actual_repr, expected_repr)

    def test_vote_str(self):
        """Method that test `__repr__` method of Vote instance object."""
        vote = Vote.objects.get(id=222)
        actual_str = vote.__str__()
        expected_str = 'id:222 event:111 is_active:True is_extended:False title:vote vote_type:1'
        self.assertMultiLineEqual(actual_str, expected_str)

    def test_vote_success_create(self):
        """Method that tests succeeded `create` method of Vote class object."""
        event = Event.objects.get(id=111)
        created_vote = Vote.create(event=event, title="my title")
        self.assertIsInstance(created_vote, Vote)

    def test_vote_unsuccess_create(self):
        """Method that tests unsuccessful `create` method of Vote class object."""
        event = Event()
        created_vote = Vote.create(event=event, title="my title")
        self.assertIsNone(created_vote)

    def test_event_update(self):
        """Method that tests `update` method of certain Vote instance."""

        actual_vote = Vote.get_by_id(111)
        actual_vote.update(is_active=True, is_extended=True, title='new title', vote_type=1)
        expected_vote = Vote.objects.get(id=111)
        self.assertEqual(actual_vote, expected_vote)

    def test_event_success_delete(self):
        """Method that tests succeeded `delete_by_id` method of Vote class object."""

        is_vote_delete = Vote.delete_by_id(111)
        self.assertTrue(is_vote_delete)

    def test_event_unsucceeded_delete(self):
        """Method that tests unsucceeded `delete_by_id` method of Vote class object."""

        id_vote_delete = Vote.delete_by_id(112)
        self.assertIsNone(id_vote_delete)


class AnswerTestCase(TestCase):
    """TestCase for Answer model"""

    def setUp(self):
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            user = CustomUser(id=111,
                              email="email1",
                              password="pass1",
                              first_name="firstname1",
                              middle_name="middle1",
                              last_name="last1")
            user.save()

            user2 = CustomUser(id=222,
                              email="email2",
                              password="pass2",
                              first_name="firstname2",
                              middle_name="middle2",
                              last_name="last2")
            user2.save()

            team = Team(id=111,
                        owner=user,
                        members=[user],
                        name='team1')
            team.save()

            event = Event(id=111,
                          team=team,
                          owner=user,
                          name='event1')
            event.save()

            vote = Vote(id=111,
                        event=event,
                        title="title",
                        vote_type=0)
            vote.save()

            answer = Answer(id=111,
                            members=[user],
                            vote=vote,
                            text='answer')

            answer.save()

    def test_answer_parameters_to_dict(self):
        answer = Answer.objects.get(id=111)
        expect_answer_dict = {'id': 111,
                              'members': [111],
                              'vote': 111,
                              'text': 'answer',
                              'create_at': 1508044512,
                              'update_at': 1508044512,
                              }
        actual_answer_dict = answer.to_dict()
        self.assertDictEqual(actual_answer_dict, expect_answer_dict)

    def test_answer_unsucceeded_get_by_id(self):
        """Method that unsucceeded tests `to_dict` method of certain Answer instance."""
        answer = Answer.get_by_id(113)
        self.assertIsNone(answer)

    def test_answer_get_by_id(self):
        """Method that tests `to_dict` method of certain Answer instance."""
        answer = Answer.get_by_id(111)
        self.assertEqual(answer.id, 111)

    def test_answer_repr(self):
        """Method that test `__repr__` method of Answer instance object."""
        answer = Answer.objects.get(id=111)

        actual_repr = answer.__repr__()
        expected_repr = '111 111 answer [111]'
        self.assertEqual(actual_repr, expected_repr)

    def test_answer_str(self):
        """Method that test `__repr__` method of Answer instance object."""
        answer = Answer.objects.get(id=111)
        actual_str = answer.__str__()
        expected_str = 'id:111 vote:111 text:answer members:[111]'
        self.assertEqual(actual_str, expected_str)

    def test_answer_success_create(self):
        """Method that tests succeeded `create` method of Answer class object."""
        vote = Vote.objects.get(id=111)
        members = CustomUser.objects.get(id=111)
        created_answer = Answer.create(members=[members], vote=vote, text='text')
        self.assertIsInstance(created_answer, Answer)

    def test_answer_unsuccess_create(self):
        """Method that tests succeeded `create` method of Answer class object."""
        vote = Vote.objects.get(id=111)
        members = CustomUser.objects.get(id=111)
        created_answer = Answer.create(members=members, vote=vote, text='text')
        self.assertIsNone(created_answer)

    def test_event_update(self):
        """Method that tests `update` method of certain Answer instance."""

        actual_answer = Answer.get_by_id(111)
        actual_answer.update(members=[111], text='new text')
        expected_answer = Answer.objects.get(id=111)
        self.assertEqual(actual_answer, expected_answer)

    def test_answer_success_delete(self):
        """Method that tests succeeded `delete_by_id` method of Answer class object."""

        id_answer_delete = Answer.delete_by_id(111)
        self.assertTrue(id_answer_delete)

    def test_answer_unsucceeded_delete(self):
        """Method that tests unsucceeded `delete_by_id` method of Answer class object."""

        id_answer_delete = Answer.delete_by_id(112)
        self.assertIsNone(id_answer_delete)
