"""
Assignment Model Test
================
This module provides complete testing for all Assignment's model functions.
"""

import datetime
from unittest import mock
from django.test import TestCase
from authentication.models import CustomUser
from assignment.models import Assignment
from curriculum.models import Curriculum
from team.models import Team
from topic.models import Topic
from item.models import Item

TEST_TIME = datetime.datetime(2017, 10, 15, 8, 15, 12)


class AssignmentModelTestCase(TestCase):
    """TestCase for providing Assignment model testing"""

    def setUp(self):
        """Method that provides preparation before testing Assignment model's features."""

        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_TIME

            custom_user = CustomUser(id=101,
                                     first_name='Jared',
                                     last_name='Leto',
                                     middle_name='Joseph',
                                     email='Jared.Leto@gmail.com',
                                     password='30sectomrs')
            custom_user.save()

            curriculum = Curriculum.objects.create(id=101,
                                                   name="testcurriculum",
                                                   goals=["goal1", "goal2"],
                                                   description="test_descr")
            curriculum.save()

            topic_python = Topic(id=101,
                                 curriculum=curriculum,
                                 title='Python',
                                 description='My awesome topic')
            topic_python.save()

            item = Item(id=101,
                        name='some name',
                        form=1,
                        topic=topic_python)
            item.save()
            item.authors.add(custom_user)

            assignment = Assignment(id=101,
                                    user=custom_user,
                                    item=item)
            assignment.save()

    def test_assignment_to_dict(self):
        """Method that tests `to_dict` method of certain Assignment instance."""

        assignment = Assignment.objects.get(id=101)
        expect_assignment_dict = {'id': 101,
                                  'statement': '',
                                  'grade': False,
                                  'user_id': 101,
                                  'item_id': 101,
                                  'status': 0,
                                  'started_at': None,
                                  'finished_at': None,
                                  'created_at': 1508044512,
                                  'updated_at': 1508044512}
        actual_assignment_dict = assignment.to_dict()

        self.assertDictEqual(actual_assignment_dict, expect_assignment_dict)

    def test_assignment_success_get_by_id(self):
        """
        Method that tests succeeded `get_by_id` method of Assignment class object.
        """

        actual_assignment = Assignment.get_by_id(101)
        expected_assignment = Assignment.objects.get(id=101)

        self.assertEqual(actual_assignment, expected_assignment)

    def test_assignment_none_get_by_id(self):
        """
        Method that tests unsucceeded `get_by_id` method of Assignment class object.
        """

        actual_assignment = Assignment.get_by_id(123)

        self.assertIsNone(actual_assignment)

    def test_assignment_success_create(self):
        """
        Method that tests succeeded `create` method of Assignment class object.
        """
        item = Item.objects.get(id=101)
        custom_user = CustomUser.objects.get(id=101)
        created_assignment = Assignment.create(user=custom_user,
                                               item=item)

        self.assertIsInstance(created_assignment, Assignment)

    def test_assignment_none_create(self):
        """
        Method that tests unsucceeded `create` method of Assignment class object.
        """
        item = Item.objects.get(id=101)
        custom_user = CustomUser()

        created_assignment = Assignment.create(user=custom_user,
                                               item=item)

        self.assertIsNone(created_assignment)

    def test_assignment_update(self):
        """
        Method that tests `update` method of certain Assignment instance.
        Test for updating only a few attributes.
        """

        actual_assignment = Assignment.get_by_id(101)

        actual_assignment.update(grade=True)
        expected_assignment = Assignment.objects.get(id=101)

        self.assertEqual(actual_assignment, expected_assignment)

    def test_assignment_all_update(self):
        """
        Method that tests `update` method of certain Assignment instance.
        Test for updating all attributes.
        """
        actual_assignment = Assignment.get_by_id(101)

        new_custom_user = CustomUser(id=1020,
                                     first_name='Jared',
                                     last_name='Leto',
                                     middle_name='Joseph',
                                     email='Jed.Leto@gmail.com',
                                     password='30sectomrs')
        new_custom_user.save()

        new_item = Item(id=1020,
                        name='some name',
                        form=1,
                        topic=Topic.get_by_id(101))
        new_item.save()
        new_item.authors.add(new_custom_user)

        actual_assignment.update(statement='some statement',
                                 grade=True,
                                 user=new_custom_user,
                                 item=new_item,
                                 status=2,
                                 started_at=datetime.datetime(2017, 4, 11, 6, 23, 11),
                                 finished_at=datetime.datetime(2017, 4, 11, 6, 23, 11))
        expected_assignment = Assignment.objects.get(id=101)

        self.assertEqual(actual_assignment, expected_assignment)

    def test_assignment_success_delete(self):
        """
        Method that tests succeeded `delete_by_id` method of Assignment class object.
        """

        is_assignment_delete = Assignment.delete_by_id(101)
        self.assertTrue(is_assignment_delete)
        self.assertRaises(Assignment.DoesNotExist, Assignment.objects.get, pk=101)

    def test_assignment_none_delete(self):
        """
        Method that tests unsucceeded `delete_by_id` method of Assignment class object.
        """

        is_assignment_delete = Assignment.delete_by_id(188)
        self.assertIsNone(is_assignment_delete)

    def test_assignment_repr(self):
        """Method that test `__repr__` magic method of Assignment instance object."""

        assignment = Assignment.objects.get(id=101)
        actual_repr = assignment.__repr__()
        expected_str = 'Assignment(id=101)'
        self.assertEqual(actual_repr, expected_str)

    def test_assignment_str(self):
        """Method that test `__str__` magic method of Assignment instance object."""

        assignment = Assignment.objects.get(id=101)
        actual_str = assignment.__str__()
        expected_str = ("'id': 101, 'statement': '', "
                        "'grade': False, 'user_id': 101, 'item_id': "
                        "101, 'status': 0, 'started_at': None, "
                        "'finished_at': None, 'created_at': 1508044512, "
                        "'updated_at': 1508044512")
        self.assertMultiLineEqual(actual_str, expected_str)

    def test_get_by_id_cache(self):
        with mock.patch('assignment.models.cache') as mock_cache:
            with mock.patch('assignment.models.pickle') as mock_pickle:
                mock_cache.__contains__.return_value = True
                mock_pickle.loads.return_value = True
                response = Assignment.get_by_id(101)
                self.assertTrue(response)

    def test_get_assignments_by_student_item_positive(self):
        assignment = Assignment.get_by_topic_item_ids(student_id=101, item_id=101)
        self.assertEqual(assignment.id, 101)

    def test_get_assignments_by_student_item_negative(self):
        assignment = Assignment.get_by_topic_item_ids(student_id=101, item_id=666)
        self.assertIsNone(assignment)

    def test_get_assignments_by_student_topic_positive(self):
        assignment = Assignment.get_by_topic_item_ids(student_id=101, topic_id=101)[0]
        self.assertEqual(assignment.id, 101)

    def test_get_assignments_by_student_positive(self):
        assignment = Assignment.get_by_topic_item_ids(student_id=101)[0]
        self.assertEqual(assignment.id, 101)

    def test_get_curriculums_positive(self):
        curriculum = Assignment.get_curriculums(101)[0]
        self.assertEqual(curriculum.id, 101)

    def test_get_topics_curriculum_id(self):
        topic = Assignment.get_topics(101, 101)[0]
        self.assertEqual(topic.id, 101)

    def test_get_topics_student_id(self):
        topic = Assignment.get_topics(101)[0]
        self.assertEqual(topic.id, 101)
