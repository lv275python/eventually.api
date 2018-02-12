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

TEST_DATE = datetime.datetime(2017, 4, 10, 12, 0, tzinfo=pytz.utc)


class TestCurriculumApp(TestCase):
    """ Tests for Curriculum app model """

    def setUp(self):
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_DATE

            self.custom_user = CustomUser.objects.create(id=1,
                                                         email='email1@mail.com',
                                                         password='1234',
                                                         first_name='1fname',
                                                         middle_name='1mname',
                                                         last_name='1lname')

            self.team = Team.objects.create(id=11,
                                            name="testteam",
                                            description="t_descr",
                                            owner=self.custom_user,
                                            image="ADSS3JHDF6DSF4JJDF")

            Curriculum.objects.create(id=111,
                                      name="testcurriculum",
                                      goals=["goal1", "goal2"],
                                      description="t_descr",
                                      team=self.team)

            Curriculum.objects.create(id=112,
                                      name="tes",
                                      goals=["goal1", "goal2"],
                                      description="t_descr",
                                      team=self.team)

    def test__str__(self):
        """ Test __str__ method"""
        expected = "'id': 111, " \
                   "'name': 'testcurriculum', " \
                   "'description': 't_descr', " \
                   "'goals': ['goal1', 'goal2'], " \
                   "'team': Team(id=11), " \
                   "'created': 1491825600, " \
                   "'updated': 1491825600"
        returned = str(Curriculum.objects.get(name="testcurriculum"))
        self.assertEqual(expected, returned)

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
        self.assertEqual(returned.team, self.team)
        self.assertEqual(returned.created_at, TEST_DATE)
        self.assertEqual(returned.updated_at, TEST_DATE)

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
        self.assertEqual(returned.team, self.team)
        self.assertEqual(returned.created_at, TEST_DATE)
        self.assertEqual(returned.updated_at, TEST_DATE)

    def test_get_by_nonexisting_name(self):
        """ Negative test get_by_name method """
        returned = Curriculum.get_by_name("nonexistingname")
        self.assertIsNone(returned)

    def test_delete_by_id(self):
        """ Positive test delete_by_id method """
        self.assertTrue(Curriculum.delete_by_id(112))

    def test_delete_by_nonexisting_id(self):
        """ Negative test delete_by_id method """
        self.assertIsNone(Curriculum.delete_by_id(100500))

    def test_create(self):
        """ Positive test create method """
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_DATE

            testcreate = Curriculum.create(name="testcreate",
                                           goals=["goal1", "goal2"],
                                           description="testcreatedescription",
                                           team=self.team)

            expected = Curriculum.objects.get(name="testcreate")

            self.assertEqual(expected.name, "testcreate")
            self.assertEqual(expected.goals, ['goal1', 'goal2'])
            self.assertEqual(expected.description, "testcreatedescription")
            self.assertEqual(expected.team, self.team)
            self.assertEqual(expected.created_at, TEST_DATE)
            self.assertEqual(expected.updated_at, TEST_DATE)

    def test_create_existing_name(self):
        """ Negative test create method """
        self.assertIsNone(Curriculum.create(name="tes"))

    def test_to_dict(self):
        """ Test to_dict method """
        expected = {'id': 111,
                    'name': 'testcurriculum',
                    'description': 't_descr',
                    'goals': ['goal1', 'goal2'],
                    'team': Team(id=11),
                    'created': 1491825600,
                    'updated': 1491825600}

        returned = Curriculum.objects.get(id=111).to_dict()

        self.assertIsInstance(returned, dict)
        self.assertEqual(expected, returned)

    def test_update(self):
        """ Positive test update method """
        Curriculum.objects.create(name="updatethis")
        objupdate = Curriculum.objects.get(name="updatethis")
        objupdate.update(name="newname",
                         description="newdescription",
                         team=self.team,)
        self.assertEqual(objupdate.name, "newname")
        self.assertEqual(objupdate.description, "newdescription")
        self.assertEqual(objupdate.team, self.team)

    def test_update_with_existing_name(self):
        """ Negative test update method """
        objupdate = Curriculum.objects.get(id=111)
        self.assertIsNone(objupdate.update(name="tes"))
