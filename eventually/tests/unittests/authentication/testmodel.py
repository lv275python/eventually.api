"""
Models' unit tests
===================
"""

from unittest import mock
import datetime
import authentication
from django.test import TestCase
from authentication.models import CustomUser
import pytz


TEST_DATE = datetime.datetime(2017, 4, 10, 12, 00, tzinfo=pytz.utc)

class TestCustomUserModel(TestCase):
    """Class for CustomUser Model test"""


    def setUp(self):
        """ Create a user object to be used by the tests """
        time_mock = datetime.datetime(2017, 4, 10, 12, 00, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = time_mock
            CustomUser(id=111,
                       email='email@mail.com',
                       password='1234',
                       first_name='fname',
                       middle_name='mname',
                       last_name='lname').save()

            CustomUser(id=4,
                       email='email_4@mail.com',
                       password='1234',
                       first_name='fname',
                       middle_name='mname',
                       last_name='lname',
                       created_at=time_mock).save()

    def test__str__(self):
        """Test of the CustomUser.__str__() method"""
        user_returned = str(CustomUser.objects.get(id=111))
        user_to_expect = "'id': 111, " \
                         "'first_name': 'fname', " \
                         "'middle_name': 'mname', " \
                         "'last_name': 'lname', " \
                         "'email': 'email@mail.com', " \
                         "'created_at': 1491825600, "\
                         "'updated_at': 1491825600, " \
                         "'is_active': False"
        self.assertEqual(user_returned, user_to_expect)

    def test__repr__(self):
        """Test of the CustomUser.__repr__() method"""
        user_returned = repr(CustomUser.objects.get(id=111))
        user_to_expect = "CustomUser(id=111)"

        self.assertEqual(user_returned, user_to_expect)

    def test_get_by_id_positive(self):
        """Positive test of the CustomUser.get_by_id() method"""
        user_returned = CustomUser.get_by_id(111)
        self.assertEqual(user_returned.id, 111)
        self.assertEqual(user_returned.email, 'email@mail.com')
        self.assertEqual(user_returned.password, '1234')
        self.assertEqual(user_returned.first_name, 'fname')
        self.assertEqual(user_returned.middle_name, 'mname')
        self.assertEqual(user_returned.last_name, 'lname')
        self.assertEqual(user_returned.created_at, TEST_DATE)
        self.assertEqual(user_returned.updated_at, TEST_DATE)
        self.assertEqual(user_returned.is_active, False)

    def test_get_by_id_with_cache_positive(self):
        """Positive test of the CustomUser.get_by_id() method"""
        with mock.patch('authentication.models.cache') as mock_cache:
            mock_cache.__contains__.return_value = True
            mock_cache.get.return_value = True
            user_returned = CustomUser.get_by_id(111)
            self.assertTrue(user_returned)

    def test_get_by_id_set_cache_positive(self):
        """Positive test of the CustomUser.get_by_id() method"""
        with mock.patch('authentication.models.cache') as mock_cache:
            mock_cache.set.return_value = True
            user_returned = CustomUser.get_by_id(111)
            self.assertTrue(user_returned)

    def test_get_by_id_negative(self):
        """Negative test of the CustomUser.get_by_id() method"""
        user_to_expect = CustomUser.get_by_id(999)
        self.assertIsNone(user_to_expect)

    def test_get_by_email_positive(self):
        """Positive test of the CustomUser.get_by_email() method"""
        user_returned = CustomUser.get_by_email('email@mail.com')
        self.assertEqual(user_returned.id, 111)
        self.assertEqual(user_returned.email, 'email@mail.com')
        self.assertEqual(user_returned.password, '1234')
        self.assertEqual(user_returned.first_name, 'fname')
        self.assertEqual(user_returned.middle_name, 'mname')
        self.assertEqual(user_returned.last_name, 'lname')
        self.assertEqual(user_returned.created_at, TEST_DATE)
        self.assertEqual(user_returned.updated_at, TEST_DATE)
        self.assertEqual(user_returned.is_active, False)

    def test_get_by_email_delete_cache_positive(self):
        """Positive test of the CustomUser.get_by_email() method"""
        # authentication.models.cache.delete('custom_user_by_email_{0}'.format('email@mail.com'))
        with mock.patch('authentication.models.cache') as mock_cache:
            mock_cache.__contains__.return_value = True
            mock_cache.get.return_value = True
            user_returned = CustomUser.get_by_email('email@mail.com')
            self.assertTrue(user_returned)

    def test_get_by_email_cache_set_positive(self):
        """Positive test of the CustomUser.get_by_email() method"""
        # authentication.models.cache.delete('custom_user_by_email_{0}'.format('email@mail.com'))
        with mock.patch('authentication.models.cache') as mock_cache:
            user_to_expect = {'id': 111,
                              'first_name': 'fname',
                              'middle_name': 'mname',
                              'last_name': 'lname',
                              'email': 'email@mail.com',
                              'created_at': 1491825600,
                              'updated_at': 1491825600,
                              'is_active': False}
            mock_cache.set.return_value = user_to_expect
            user_returned = CustomUser.get_by_email('email@mail.com')
            self.assertEqual(user_returned.id, 111)
            self.assertEqual(user_returned.email, 'email@mail.com')
            self.assertEqual(user_returned.password, '1234')
            self.assertEqual(user_returned.first_name, 'fname')
            self.assertEqual(user_returned.middle_name, 'mname')
            self.assertEqual(user_returned.last_name, 'lname')
            self.assertEqual(user_returned.created_at, TEST_DATE)
            self.assertEqual(user_returned.updated_at, TEST_DATE)
            self.assertEqual(user_returned.is_active, False)

    def test_get_by_email_negative(self):
        """Negative test of the CustomUser.get_by_email() method"""
        user_to_expect = CustomUser.get_by_email('doesnotexist@mail.com')
        self.assertIsNone(user_to_expect)

    def test_delete_by_id_positive(self):
        """ Test of the CustomUser.delete_by_id() method """
        self.assertTrue(CustomUser.delete_by_id(4))
        self.assertRaises(CustomUser.DoesNotExist, CustomUser.objects.get, pk=4)

    def test_delete_by_id_negative(self):
        """ Test of the CustomUser.delete_by_id() method """
        CustomUser.delete_by_id(89)
        self.assertIsNone(CustomUser.delete_by_id(41))

    def test_create_positive(self):
        """ Positive Test of the CustomUser.create method """
        time_mock = datetime.datetime(2017, 4, 10, 12, 00, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now') as mock_time:
            with mock.patch('authentication.models.cache') as mock_cache:
                mock_cache.__contains__.return_value = True
                mock_time.return_value = time_mock
                user_returned = CustomUser.create('email_new@mail.com', '1234',
                                                  'fname', 'mname', 'lname')
                self.assertIsInstance(user_returned, CustomUser)
                self.assertEqual(user_returned.email, 'email_new@mail.com')
                self.assertEqual(user_returned.first_name, 'fname')
                self.assertEqual(user_returned.middle_name, 'mname')
                self.assertEqual(user_returned.last_name, 'lname')
                self.assertEqual(user_returned.created_at, TEST_DATE)
                self.assertEqual(user_returned.updated_at, TEST_DATE)
                self.assertEqual(user_returned.is_active, False)

    def test_create_negative(self):
        """ Negative Test of the CustomUser.create() method """
        CustomUser.create('96@mail.com', '1234', 'fname', 'mname', 'lname')
        expect_none = CustomUser.create('96@mail.com', '1234', 'fname', 'mname', 'lname')
        self.assertIsNone(expect_none)

    def test_to_dict(self):
        """ Test of the CustomUser.create() method """
        user_returned = CustomUser.objects.get(id=111)
        user_to_expect = {'id': 111,
                          'first_name': 'fname',
                          'middle_name': 'mname',
                          'last_name': 'lname',
                          'email': 'email@mail.com',
                          'created_at': 1491825600,
                          'updated_at': 1491825600,
                          'is_active': False}
        self.assertEqual(user_returned.to_dict(), user_to_expect)

    def test_update(self):
        """ Test of the CustomUser.create(args) method """
        with mock.patch('authentication.models.cache') as mock_cache:
            mock_cache.__contains__.return_value = True
            user_to_update = CustomUser.objects.get(id=4)
            user_to_update.update('John', 'Smith', 'Jr.', '123456', True)
            user_to_expect = CustomUser(id=4,
                                        password='123456',
                                        first_name='John',
                                        middle_name='mnSmithame',
                                        last_name='Jr.',
                                        is_active=True)
            self.assertEqual(user_to_update, user_to_expect)

    def test_get_all_users_cache(self):
        """ Test of the CustomUser.get_all() method  with cache"""
        with mock.patch('authentication.models.cache') as mock_cache:
            with mock.patch('pickle.loads') as mock_pickle:
                mock_cache.__contains__.return_value = True
                mock_pickle.return_value = CustomUser.objects.all()
                expected_value = CustomUser.objects.all()
                current_value = CustomUser.get_all()
                self.assertListEqual(list(current_value), list(expected_value))

    def test_get_all_users_pickle(self):
        """ Test of the CustomUser.get_all() method """
        with mock.patch('pickle.loads') as mock_pickle:
            mock_pickle.return_value = CustomUser.objects.all()
            expected_value = CustomUser.objects.all()
            current_value = CustomUser.get_all()
            self.assertListEqual(list(current_value), list(expected_value))

    def test_delete_by_id_cache(self):
        """ Test of the CustomUser.delete_by_id() method """
        with mock.patch('authentication.models.cache') as mock_cache:
            mock_cache.__contains__.return_value = True
            authentication.models.cache.set("all_users", None)
            user_returned = CustomUser.delete_by_id(111)
            self.assertTrue(user_returned)
