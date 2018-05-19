"""
 Vote view tests
 ===============

 This module provides complete testing for all Vote's views functions.
 """

import json
import datetime
import pytz
from unittest.mock import patch

from authentication.models import CustomUser
from django.test import TestCase, Client
from customprofile.models import CustomProfile
from django.core.urlresolvers import reverse
from team.models import Team
from event.models import Event
from vote.models import Vote, Answer
from unittest import mock

TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12)
TEST_CREATED_AT = datetime.datetime(2017, 4, 10, 12, 00, tzinfo=pytz.utc)



class VoteViewTest(TestCase):
    """TestCase for providing Vote view testing."""

    def setUp(self):
        """Method that provides preparation before testing Vote view's features."""
        custom_user = CustomUser.objects.create(id=111,
                                                email='email@gmail.com',
                                                is_active=True)
        custom_user.set_password('123Qwerty')
        custom_user.save()

        self.client = Client()
        self.client.login(username='email@gmail.com',
                          password='123Qwerty')

        team = Team.objects.create(id=111,
                                   owner=custom_user,
                                   members=[custom_user],
                                   name='team1')

        event = Event.objects.create(id=111,
                                     team=team,
                                     owner=custom_user,
                                     name='event1')

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME
            vote = Vote.objects.create(id=111,
                                       event=event,
                                       is_active=True,
                                       is_extended=True,
                                       title="my title",
                                       vote_type=0)
            vote.save()

    def test_success_get(self):
        """Method that tests the successful get request of vote"""
        url = reverse('event:vote:detail', args=[111, 111, 111])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        custom_user = CustomUser.objects.create(id=222, email='exp@gmail.com', is_active=True)
        custom_user.set_password('123Qwerty')
        custom_user.save()
        team = Team.objects.create(id=222, owner=custom_user, members=[custom_user], name='name')
        team.save()
        event = Event.objects.create(id=222, team=team, owner=custom_user, name='name')
        event.save()
        vote = Vote.objects.create(id=222, event=event, title="new title", vote_type=0)
        vote.save()

        url = reverse('event:vote:detail', args=[222, 222, 222])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


    def test_success_get_all(self):
        """Method that tests the successful get all votes"""
        url = reverse('event:vote:index', args=[111, 111])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_error_invalid_vote_get(self):
        """Method that test invalid get request for the certain vote"""

        url = reverse('event:vote:detail', args=[111, 111, 100])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_error_invalid_user_id_get(self):
        """Method that tests unsuccessful get request with invalid user id data"""
        custom_user = CustomUser.objects.create(id=222, email='exp@gmail.com', is_active=True)
        custom_user.set_password('123Qwerty')
        custom_user.save()
        team = Team.objects.create(id=222, owner=custom_user, members=[custom_user], name='name')
        team.save()
        event = Event.objects.create(id=222, team=team, owner=custom_user, name='name')
        event.save()
        vote = Vote.objects.create(id=222, event=event, title="new title", vote_type=0)
        vote.save()

        url = reverse('event:vote:detail', args=[222, 222, 222])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_error_invalid_event_id_post(self):
        """Method that tests unsuccessful post request with invalid event id"""

        data = {'title': '',
                'is_active': False}

        url = reverse('event:vote:index', args=[111, 101])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_success_vote_post(self):
        """Method that tests successful post request with invalid vote."""

        data = {'title': 'qqq',
                'is_active': False,
                'vote_type': 1}

        url = reverse('event:vote:index', args=[111, 111])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_unsuccessful_vote_post(self):
        """Method that tests unsuccessful post request with invalid vote."""

        custom_user = CustomUser.objects.create(id=222, email='exp@gmail.com', is_active=True)
        custom_user.set_password('123Qwerty')
        custom_user.save()
        team = Team.objects.create(id=222, owner=custom_user, members=[custom_user], name='name')
        team.save()
        event = Event.objects.create(id=222, team=team, owner=custom_user, name='name')
        event.save()

        with mock.patch('vote.models.Vote.create') as new_create:
            new_create.return_value = None
            data = {'title': 'qqq',
                    'is_active': False}

            url = reverse('event:vote:index', args=[222, 222])
            response = self.client.post(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_error_invalid_data_validate(self):
        """Method that tests unsuccessful post request with invalid JSON data."""

        data = {}
        url = reverse('event:vote:index', args=[111, 111])
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_success_put(self):
        """Method that test invalid put request for the updating the certain vote"""

        data = {'title': 'test title',
                'is_active': False}

        url = reverse('event:vote:detail', args=[111, 111, 111])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_error_invalid_vote_put(self):
        """Method that tests unsuccessful put request with invalid vote """

        data = {'title': 'test title',
                'is_active': False}

        url = reverse('event:vote:detail', args=[111, 111, 10])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_invalid_json_put(self):
        """Method that tests unsuccessful put request with invalid JSON accepted data"""

        data = {}

        url = reverse('event:vote:detail', args=[111, 111, 111])
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_invalid_vote_id_put(self):
        """Method that test invalid delete request for the updating the certain vote"""

        data = {'title': 'test title',
                'is_active': False}

        url = reverse('event:vote:index', args=[111, 111])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_invalid_user_id_put(self):
        """Method that tests unsuccessful put request with invalid user id data"""
        custom_user = CustomUser.objects.create(id=222, email='exp@gmail.com', is_active=True)
        custom_user.set_password('123Qwerty')
        custom_user.save()
        team = Team.objects.create(id=222, owner=custom_user, members=[custom_user], name='name')
        team.save()
        event = Event.objects.create(id=222, team=team, owner=custom_user, name='name')
        event.save()
        vote = Vote.objects.create(id=222, event=event, title="new title", vote_type=0)
        vote.save()

        data = {'title': 'test title',
                'is_active': False}

        url = reverse('event:vote:detail', args=[222, 222, 222])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_success_delete(self):
        """Method that test invalid delete request for the updating the certain vote"""

        url = reverse('event:vote:detail', args=[111, 111, 111])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_error_invalid_vote_delete(self):
        """Method that test invalid delete request for the updating the certain vote"""

        url = reverse('event:vote:detail', args=[111, 111, 12])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_error_invalid_vote_id_delete(self):
        """Method that test invalid delete request for the updating the certain vote"""

        url = reverse('event:vote:index', args=[111, 111])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)

    def test_error_invalid_user_id_delete(self):
        """Method that tests unsuccessful delete request with invalid user id data"""
        custom_user = CustomUser.objects.create(id=222, email='exp@gmail.com', is_active=True)
        custom_user.set_password('123Qwerty')
        custom_user.save()
        team = Team.objects.create(id=222, owner=custom_user, members=[custom_user], name='name')
        team.save()
        event = Event.objects.create(id=222, team=team, owner=custom_user, name='name')
        event.save()
        vote = Vote.objects.create(id=222, event=event, title="new title", vote_type=0)
        vote.save()

        url = reverse('event:vote:detail', args=[222, 222, 222])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)


class AnswerViewTest(TestCase):
    """TestCase for providing Answer view testing."""

    def setUp(self):
        """Method that provides preparation before testing Vote view's features."""
        custom_user = CustomUser.objects.create(id=111,
                                                email='email@gmail.com',
                                                first_name="Robert",
                                                last_name="Downey",
                                                middle_name="Jr.",
                                                is_active=True)
        custom_user.set_password('123Qwerty')
        custom_user.save()

        self.client = Client()
        self.client.login(username='email@gmail.com',
                          password='123Qwerty')

        team = Team.objects.create(id=111,
                                   owner=custom_user,
                                   members=[custom_user],
                                   name='team1')

        event = Event.objects.create(id=111,
                                     team=team,
                                     owner=custom_user,
                                     name='event1')

        vote = Vote.objects.create(id=111,
                                   event=event,
                                   is_active=True,
                                   is_extended=True,
                                   title="my title",
                                   vote_type=0)


        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            answer = Answer.objects.create(id=111,
                                           members=[custom_user],
                                           vote=vote,
                                           text="answer")
            answer.save()
            mock_time.return_value = TEST_CREATED_AT

            custom_profile = CustomProfile.objects.create(id=222,
                                                          user=custom_user,
                                                          hobby='box',
                                                          photo='link1',
                                                          birthday='2000-2-4',
                                                          created_at=TEST_CREATED_AT,
                                                          updated_at=TEST_CREATED_AT)
            custom_profile.save()

        custom_user = CustomUser.objects.create(id=222,
                                                email='expqqq@gmail.com',
                                                is_active=True)
        custom_user.set_password('123Qwerty')
        custom_user.save()

        team = Team.objects.create(id=222,
                                   owner=custom_user,
                                   members=[custom_user],
                                   name='name')

        event = Event.objects.create(id=222,
                                     team=team,
                                     owner=custom_user,
                                     name='name')

        vote = Vote.objects.create(id=222,
                                   event=event,
                                   title="new title",
                                   vote_type=0)

        answer = Answer.objects.create(id=222,
                                       vote=vote,
                                       members=[custom_user],
                                       text="title")


    def test_success_get(self):
        """Method that tests the successful get request of vote"""
        url = reverse('event:vote:answer_detail', args=[111, 111, 111, 111])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_success_get_all(self):
        """Method that tests the successful get request of vote"""
        url = reverse('event:vote:answer', args=[111, 111, 111])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_error_invalid_answer_get(self):
        """Method that test invalid get request for the certain answer"""

        url = reverse('event:vote:answer_detail', args=[111, 111, 111, 100])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_error_invalid_user_id_get(self):
        """Method that tests unsuccessful get request with invalid user id data"""

        url = reverse('event:vote:answer_detail', args=[222, 222, 222, 222])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_error_invalid_vote_id_post(self):
        """Method that tests unsuccessful post request with invalid vote id"""

        data = {'text': ''}

        url = reverse('event:vote:answer', args=[111, 111, 110])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_success_answer_post(self):
        """Method that tests successful post request with answer."""
        data = {'text': 'qqq',
                'members': [111]}

        url = reverse('event:vote:answer', args=[111, 111, 111])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_unsuccessful_vote_post(self):
        """Method that tests unsuccessful post request with invalid vote."""

        custom_user = CustomUser.objects.create(id=333, email='exp@gmail.com', is_active=True)
        custom_user.set_password('123Qwerty')
        custom_user.save()
        team = Team.objects.create(id=333, owner=custom_user, members=[custom_user], name='name')
        team.save()
        event = Event.objects.create(id=333, team=team, owner=custom_user, name='name')
        event.save()
        vote = Vote.objects.create(id=333, event=event, title="new title", vote_type=0)
        vote.save()

        with mock.patch('vote.models.Vote.create') as new_create:
            new_create.return_value = None
            data = {'text': 'qqq'}
            url = reverse('event:vote:answer', args=[333, 333, 333])
            response = self.client.post(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_error_invalid_json_post(self):
        """Method that tests unsuccessful post request with invalid JSON data."""

        data = {}
        url = reverse('event:vote:answer', args=[111, 111, 111])
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_success_put(self):
        """Method that test invalid put request for the updating the certain answer"""

        data = {'text': 'test title'}

        url = reverse('event:vote:answer_detail', args=[111, 111, 111, 111])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_error_invalid_vote_put(self):
        """Method that tests unsuccessful put request with invalid answer """

        data = {'text': 'test title'}

        url = reverse('event:vote:answer_detail', args=[111, 111, 111, 10])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_error_invalid_json_put(self):
        """Method that tests unsuccessful put request with invalid JSON accepted data"""

        data = {}

        url = reverse('event:vote:answer_detail', args=[111, 111, 111, 111])
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_invalid_answer_id_put(self):
        """Method that test invalid delete request for the updating the certain answer"""

        data = {'text': 'test title'}

        url = reverse('event:vote:answer', args=[111, 111, 111])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_error_invalid_user_id_put(self):
        """Method that tests unsuccessful put request with invalid user id data"""

        data = {'text': 'test text'}

        url = reverse('event:vote:answer_detail', args=[222, 222, 222, 222])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_success_delete(self):
        """Method that test invalid delete request for the updating the certain vote"""

        url = reverse('event:vote:answer_detail', args=[111, 111, 111, 111])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_error_invalid_answer_delete(self):
        """Method that test invalid delete request for the updating the certain answer"""

        url = reverse('event:vote:answer_detail', args=[111, 111, 111, 12])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_error_invalid_answer_id_delete(self):
        """Method that test invalid delete request for the updating the certain answer"""

        url = reverse('event:vote:answer', args=[111, 111, 111])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)

    def test_error_invalid_user_id_delete(self):
        """Method that tests unsuccessful delete request with invalid user id data"""

        url = reverse('event:vote:answer_detail', args=[222, 222, 222, 222])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_get_answers_with_members(self):
        """
        Method that tests response with answers data for specific vote
        """
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME
            custom_user = CustomUser.objects.create(id=227,
                                                    email='expqweq@gmail.com',
                                                    is_active=True)
            custom_user.set_password('123Qwerty')
            custom_user.save()

            team = Team.objects.create(id=227,
                                       owner=custom_user,
                                       members=[custom_user],
                                       name='name')

            event = Event.objects.create(id=227,
                                         team=team,
                                         owner=custom_user,
                                         name='name')

            vote = Vote.objects.create(id=227,
                                       event=event,
                                       title="new title",
                                       vote_type=0)


            answer = Answer.objects.create(id=227,
                                           members=[custom_user],
                                           vote=vote,
                                           text="answer")

            mock_time.return_value = TEST_CREATED_AT

            custom_profile = CustomProfile.objects.create(id=227,
                                                          user=custom_user,
                                                          hobby='box',
                                                          photo='link1',
                                                          birthday='2000-2-4',
                                                          created_at=TEST_CREATED_AT,
                                                          updated_at=TEST_CREATED_AT)
            custom_profile.save()
            self.client.login(username='expqweq@gmail.com',
                              password='123Qwerty')
            url = reverse('events:vote:answers_with_members', args=[227, 227])
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)

    def test_error_invalid_answers_with_members_(self):
        """
        Method that tests response with answers data for specific vote
        """
        url = reverse('events:vote:answers_with_members', args=[227, 228])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_error_invalid_json_answers_with_members_(self):
        """
        Method that tests response with answers data for specific vote
        """

        data = {}
        url = reverse('events:vote:answers_with_members', args=[227, 228])
        response = self.client.delete(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
