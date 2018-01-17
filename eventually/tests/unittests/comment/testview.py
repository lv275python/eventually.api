"""
Comment Views Test.
==================

This module provides complete testing for all Comment's views functions.
"""
import json
import datetime
from django.test import TestCase, Client
from authentication.models import CustomUser
from django.core.urlresolvers import reverse
from django.utils import timezone
from unittest import mock
from comment.models import Comment
from event.models import Event
from task.models import Task
from team.models import Team
from vote.models import Vote
from comment.views import CommentView



TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12, 0, tzinfo=timezone.utc)


class Comment_View_Test(TestCase):
    """TestCase for providing Comment view testing."""
    def setUp(self):
        """Method that provides preparation before testing Event view's features."""
        custom_user = CustomUser.objects.create(id=100, email='email@gmail.com', is_active=True)
        custom_user.set_password('Aa123456')
        custom_user.save()

        receiver = CustomUser.objects.create(id=1500, email='receiver@gmail.com', is_active=True)
        receiver.set_password('123456')
        receiver.save()

        second_custom_user = CustomUser.objects.create(id=200, email='qwerty@gmail.com', is_active=True)
        second_custom_user.set_password('Aaqwerty11')
        second_custom_user.save()

        self.client = Client()
        self.client.login(username='email@gmail.com', password='Aa123456')

        team = Team.objects.create(id=1000,
                                   owner=custom_user,
                                   members=[custom_user],
                                   name='barcelona')

        event = Event.objects.create(id=1000,
                                     owner=custom_user,
                                     name='some name')

        task = Task.objects.create(id=1000,
                                   title='text',
                                   description='text',
                                   status=0,
                                   users=[custom_user],
                                   event=event)

        vote = Vote.objects.create(id=1000,
                                   title='text',
                                   event=event,
                                   vote_type=0)



        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME
            first_comment = Comment.objects.create(id=100, team=team, author=custom_user,
                                                   text='football', receiver=receiver)
            second_comment = Comment.objects.create(id=200, team=team, event=event, author=second_custom_user,
                                                    text='some_sport', receiver=receiver)
            third_comment = Comment.objects.create(id=300, team=team, event=event, task=task, author=second_custom_user,
                                                   text='any_sport', receiver=receiver)
            fourth_comment = Comment.objects.create(id=400, team=team, event=event, vote=vote, author=second_custom_user,
                                                    text='sport', receiver=receiver)

    def test_get_success_with_event(self):
        """
        Method that tests the successful get request for the certain comment of the certain event.
        """
        data = {
            "id": 200,
            "text": 'some_sport',
            "created_at": int(TEST_TIME.timestamp()),
            "updated_at": int(TEST_TIME.timestamp()),
            "team": 1000,
            "event": 1000,
            "task": None,
            "vote": None,
            "author": 200,
            "receiver": 1500
        }
        url = reverse('event:comment:detail', args=[1000, 1000, 200])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(data))

    def test_get_fail_no_id_with_team(self):
        """
        Method that tests the successful get request for the certain comment of the certain team.
        """
        data = {'comments': [Comment.get_by_id(100).to_dict(),
                             Comment.get_by_id(200).to_dict(),
                             Comment.get_by_id(300).to_dict(),
                             Comment.get_by_id(400).to_dict()]
        }
        url = reverse('comment:index', args=[1000])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(data))

    def test_get_fail_no_id_with_event(self):
        """
        Method that tests the successful get request for the certain comment of the certain event.
        """
        data = {'comments': [Comment.get_by_id(200).to_dict(),
                             Comment.get_by_id(300).to_dict(),
                             Comment.get_by_id(400).to_dict()]
        }
        url = reverse('event:comment:index', args=[1000, 1000])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(data))

    def test_get_fail_no_id_with_task(self):
        """
        Method that tests the successful get request for the certain comment of the certain task.
        """
        data = {'comments': [Comment.get_by_id(300).to_dict()]
        }
        url = reverse('event:task:comment:index', args=[1000, 1000, 1000])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(data))

    def test_get_fail_no_id_with_vote(self):
        """
        Method that tests the successful get request for the certain comment of the certain vote.
        """
        data = {'comments': [Comment.get_by_id(400).to_dict()]
        }
        url = reverse('event:vote:comment:index', args=[1000, 1000, 1000])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(data))



    def test_get_fail_wrong_id(self):
        """
        Method that tests the unsuccessful get request
        for the certain comment of the certain team.
        Wrong comment id in url.
        """
        url = reverse('comment:detail', args=[1000, 101])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_success(self):
        """
        Method that tests the successful post request for creating of comment.
        """
        data = {
            "text": 'some_text'
        }
        url = reverse('comment:index', args=[1000])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_post_fail_wrong_id(self):
        """
        Method that tests the unsuccessful post request for creating of comment.
        Wrong team id in url.
        """
        data = {
            "text": 'some_text'
        }
        url = reverse('comment:index', args=[1001])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_post_fail_bad_json(self):
        """
        Method that tests the unsuccessful post request for creating of comment.
        Bad json file.
        """
        data = {
            "text": 1
        }
        url = reverse('comment:index', args=[1000])
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)


    def test_post_fail_db_create(self):
        """
        Method that tests the unsuccessful post request for creating of comment.
        db error.
        """
        with mock.patch('comment.models.Comment.create') as comment_create:
            comment_create.return_value = None

            data = {
                "text": 'some text'
            }
            url = reverse('comment:index', args=[1000])
            response = self.client.post(url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 400)



    def test_put_success(self):
        """
        Method that tests the successful put request
        for the certain comment of the certain team.
        """
        data = {
            "text": 'some_text'
        }
        url = reverse('comment:detail', args=[1000, 100])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_fail_bad_json(self):
        """
        Method that tests the unsuccessful put request
        for the certain comment of the certain team.
        Bad Json file.
        """
        data = {
            "text": 1
        }
        url = reverse('comment:detail', args=[1000, 100])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_fail_wrong_id(self):
        """
        Method that tests the unsuccessful put request
        for the certain comment of the certain team.
        Wrong comment id in url.
        """
        data = {
            "text": 'some_text'
        }
        url = reverse('comment:detail', args=[1000, 101])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_put_fail_no_permission(self):
        """
        Method that tests the unsuccessful put request
        for the certain comment of the certain team.
        No permission for request.user.
        """
        data = {
            "text": 'some_text'
        }
        url = reverse('comment:detail', args=[1000, 200])
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_delete_success(self):
        """
        Method that tests the successful delete request
        for the certain comment of the certain team.
        """
        url = reverse('comment:detail', args=[1000, 100])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_fail_wrong_id(self):
        """
        Method that tests the unsuccessful delete request
        for the certain comment of the certain team.
        Wrong comment id in url.
        """
        url = reverse('comment:detail', args=[1000, 101])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_fail_no_permission(self):
        """
        Method that tests the unsuccessful delete request
        for the certain comment of the certain team.
        No permission for request.user.
        """
        url = reverse('comment:detail', args=[1000, 200])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
