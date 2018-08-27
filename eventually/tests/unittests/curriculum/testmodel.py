"""
Curriculum Model tests
======================
"""

from unittest import mock
import datetime
import pytz
from django.test import TestCase
from authentication.models import CustomUser
from curriculum.models import Curriculum
from team.models import Team

TEST_DATE = datetime.datetime(2017, 10, 30, 6, 15, 12, tzinfo=pytz.utc)


class TestCurriculumApp(TestCase):
    """ Tests for Curriculum app model """

    def setUp(self):
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_DATE
            custom_user = CustomUser.objects.create(id=1,
                                                    email='email1@mail.com',
                                                    password='1234',
                                                    first_name='1fname',
                                                    middle_name='1mname',
                                                    last_name='1lname')
            custom_user.set_password('1234')
            custom_user.save()

            Curriculum.objects.create(id=111,
                                      name="testcurriculum",
                                      goals=["goal1", "goal2"],
                                      description="t_descr",
                                      owner=custom_user)

            Curriculum.objects.create(id=112,
                                      name="tes",
                                      goals=["goal1", "goal2"],
                                      description="t_descr",
                                      owner=custom_user)

    def test__repr__(self):
        """ Test __repr__ method """
        expected = "Curriculum(id=111)"
        returned = repr(Curriculum.objects.get(name="testcurriculum"))
        self.assertEqual(expected, returned)

    def test_get_by_id(self):
        """ Positive test get_by_id method"""
        returned = Curriculum.get_by_id(111)

        self.assertEqual(returned.id, 111)
        self.assertEqual(returned.name, "testcurriculum")
        self.assertEqual(returned.goals, ['goal1', 'goal2'])
        self.assertEqual(returned.description, "t_descr")
        self.assertEqual(returned.created_at, TEST_DATE)
        self.assertEqual(returned.updated_at, TEST_DATE)

    def test_get_by_id_cache(self):
        """ Test for access to the cache in get_by_id method"""
        with mock.patch('curriculum.models.cache') as mock_cache:
            with mock.patch('curriculum.models.pickle') as mock_pickle:
                mock_cache.__contains__.return_value = True
                mock_pickle.load.return_value = True
                returned = Curriculum.get_by_id(111)
                self.assertTrue(returned)

    def test_get_by_nonexisting_id(self):
        """ Negative test get_by_id method """
        returned = Curriculum.get_by_id(100500)
        self.assertIsNone(returned)

    def test_get_by_name(self):
        """ Positive test get_by_name method """
        returned = Curriculum.get_by_name("testcurriculum")

        self.assertEqual(returned.id, 111)
        self.assertEqual(returned.name, "testcurriculum")
        self.assertEqual(returned.goals, ['goal1', 'goal2'])
        self.assertEqual(returned.description, "t_descr")
        self.assertEqual(returned.created_at, TEST_DATE)
        self.assertEqual(returned.updated_at, TEST_DATE)

        with mock.patch('curriculum.models.cache') as mock_cache:
            with mock.patch('curriculum.models.pickle') as mock_pickle:
                mock_cache.__contains__.return_value = True
                mock_pickle.load.return_value = True
                returned = Curriculum.get_by_name("testcurriculum")
                self.assertTrue(returned)

    def test_get_by_name_cache(self):
        """ Test for access to the cache in get_by_name method"""
        with mock.patch('curriculum.models.cache') as mock_cache:
            with mock.patch('curriculum.models.pickle') as mock_pickle:
                mock_cache.__contains__.return_value = True
                mock_pickle.load.return_value = True
                returned = Curriculum.get_by_name("testcurriculum")
                self.assertTrue(returned)

    def test_get_by_nonexisting_name(self):
        """ Negative test get_by_name method """
        returned = Curriculum.get_by_name("nonexistingname")
        self.assertIsNone(returned)

    def test_delete_by_id(self):
        """ Positive test delete_by_id method """
        self.assertTrue(Curriculum.delete_by_id(112))
        with mock.patch('curriculum.models.cache') as mock_cache:
            with mock.patch('curriculum.models.pickle') as mock_pickle:
                mock_cache.__contains__.return_value = True
                mock_pickle.load.return_value = True
                returned = Curriculum.get_by_name("testcurriculum")
                self.assertTrue(returned)

    def test_delete_by_nonexisting_id(self):
        """ Negative test delete_by_id method """
        self.assertIsNone(Curriculum.delete_by_id(100500))

    def test_create(self):
        """ Positive test create method """
        with mock.patch('django.utils.timezone.now') as mock_time:
            with mock.patch('curriculum.models.cache') as mock_cache:
                mock_cache.__contains__.return_value = True
                mock_time.return_value = TEST_DATE

                owner = CustomUser.objects.get(id=1)

                testcreate = Curriculum.create(name="testcreate",
                                               goals=["goal1", "goal2"],
                                               description="testcreatedescription",
                                               owner=owner)

                expected = Curriculum.objects.get(name="testcreate")

                self.assertEqual(expected.name, "testcreate")
                self.assertEqual(expected.goals, ['goal1', 'goal2'])
                self.assertEqual(expected.description, "testcreatedescription")
                self.assertEqual(expected.owner, owner)
                self.assertEqual(expected.created_at, TEST_DATE)
                self.assertEqual(expected.updated_at, TEST_DATE)
                self.assertTrue(testcreate)

    def test_create_existing_name(self):
        """ Negative test create method """
        owner = CustomUser.objects.get(id=1)
        self.assertIsNone(Curriculum.create(name="tes", owner=owner))

    def test_to_dict(self):
        """ Test to_dict method """
        owner = CustomUser.objects.get(id=1)
        expected = {'id': 111,
                    'name': 'testcurriculum',
                    'description': 't_descr',
                    'goals': ['goal1', 'goal2'],
                    'owner': 1,
                    'created': 1509344112,
                    'updated': 1509344112}

        returned = Curriculum.objects.get(id=111).to_dict()

        self.assertIsInstance(returned, dict)
        self.assertEqual(expected, returned)

    def test_update(self):
        """ Positive test update method """
        curriculum_object = Curriculum.objects.create(name="updatethis")
        objupdate = Curriculum.objects.get(name="updatethis")

        with mock.patch('curriculum.models.cache') as mock_cache:
            mock_cache.__contains__.return_value = True
            owner = CustomUser.objects.get(id=1)
            update = objupdate.update(name="newname",
                                      description="newdescription",
                                      owner=owner)

        self.assertEqual(objupdate.name, "newname")
        self.assertEqual(objupdate.description, "newdescription")
        self.assertTrue(update)

    def test_update_with_existing_name(self):
        """ Negative test update method """
        owner = CustomUser.objects.get(id=1)
        objupdate = Curriculum.objects.get(id=111)
        self.assertIsNone(objupdate.update(name="tes", owner=owner))

    def test_get_all(self):
        """Test for get_all method"""
        expected_object = Curriculum.objects.all()
        current_value = Curriculum.get_all()
        self.assertEqual(list(current_value), list(expected_object))

        with mock.patch('curriculum.models.cache') as mock_cache:
            with mock.patch('curriculum.models.pickle') as mock_pickle:
                mock_cache.__contains__.return_value = True
                mock_pickle.load.return_value = True
                returned = Curriculum.get_by_name("testcurriculum")
                self.assertTrue(returned)

    def test_get_all_cache(self):
        """Tests the access to cache in get_all method"""
        with mock.patch('curriculum.models.cache') as mock_cache:
            with mock.patch('curriculum.models.pickle') as mock_pickle:
                mock_cache.__contains__.return_value = True
                mock_pickle.loads.return_value = True
                self.assertTrue(Curriculum.get_all())
