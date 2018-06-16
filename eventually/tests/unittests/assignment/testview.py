# """
# Assignment View tests
# ======================
# """
#
# import json
# import datetime
# from authentication.models import CustomUser
# from django.test import TestCase, Client
# from django.core.urlresolvers import reverse
# from assignment.models import Assignment
# from item.models import Item
# from curriculum.models import Curriculum
# from topic.models import Topic
# from unittest import mock
#
# TEST_TIME = datetime.datetime(2017, 10, 30, 8, 15, 12)
#
# class TestAssignmentApp(TestCase):
#     """ Tests for Curriculum app model """
#
#     def setUp(self):
#
#         custom_user = CustomUser.objects.create(id=1,
#                                                 email='email.1@mail.com',
#                                                 first_name='1fname',
#                                                 middle_name='1mname',
#                                                 last_name='1lname',
#                                                 is_active=True)
#         custom_user.set_password('1111')
#         custom_user.save()
#
#         custom_user = CustomUser.objects.create(id=2,
#                                                 email='email.2@mail.com',
#                                                 first_name='2fname',
#                                                 middle_name='2mname',
#                                                 last_name='2lname',
#                                                 is_active=True)
#
#         custom_user.set_password('1111')
#         custom_user.save()
#
#         self.client = Client()
#         self.client.login(username='email.1@mail.com', password='1111')
#
#         Curriculum.objects.create(id=111,
#                                   name="testcurriculum",
#                                   goals=["goal1", "goal2"],
#                                   description="some_description",
#                                   team=None)
#
#         Topic.objects.create(id=222,
#                              curriculum=Curriculum.get_by_id(111),
#                              author=CustomUser.get_by_id(1),
#                              title='Topic #1',
#                              description="test_description",
#                              mentors=(CustomUser.get_by_id(1),))
#
#         Topic.objects.create(id=223,
#                              curriculum=Curriculum.get_by_id(111),
#                              author=CustomUser.get_by_id(2),
#                              title='Topic #1',
#                              description="test_description",
#                              mentors=(CustomUser.get_by_id(2),))
#
#         Item.objects.create(id=333,
#                             topic=Topic.get_by_id(222),
#                             authors=(CustomUser.get_by_id(1), ),
#                             name='Item #1',
#                             form=0,
#                             description='description')
#
#         Item.objects.create(id=334,
#                             topic=Topic.get_by_id(222),
#                             authors=(CustomUser.get_by_id(1), ),
#                             name='Item #2',
#                             form=0,
#                             description='description',
#                             superiors=[333])
#
#         Item.objects.create(id=335,
#                             topic=Topic.get_by_id(223),
#                             authors=(CustomUser.get_by_id(1), ),
#                             name='Item #3',
#                             form=0,
#                             description='description')
#
#         Assignment.objects.create(id=444,
#                                   user=CustomUser.get_by_id(1),
#                                   item=Item.get_by_id(333))
#
#         Assignment.objects.create(id=445,
#                                   user=CustomUser.get_by_id(1),
#                                   item=Item.get_by_id(334))
#
#     def test_success_get_by_id(self):
#         """Method that tests the successful get request for the Assignment with the certain id"""
#         with mock.patch('django.utils.timezone.now') as mock_time:
#             mock_time.return_value = TEST_TIME
#
#             Assignment.objects.create(
#                 # id=111,
#                 statement='my_statement1',
#                 grade=4.5,
#                 user=CustomUser.get_by_id(1),
#                 item=None,
#                 status=2
#             )
#
#             expected_data = {
#                 'new_date':
#                     [
#                         {'statuses': 2, 'statements': "my_statement1"}
#                     ]
#             }
#
#             url = reverse('AssignmentAnswer')
#             response = self.client.get(url)
#             self.assertEqual(response.status_code, 201)
#             self.assertJSONEqual(response.content.decode('utf-8'), json.dumps(expected_data))
#
#     def test_failed_get_by_id(self):
#         """Method that tests the successful get request for the Assignment with the certain id"""
#
#         url = reverse('AssignmentAnswer')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 404)
