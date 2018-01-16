from authentication.models import CustomUser
from django.test import TestCase
from utils import team_views_functions


class UtilsTeamViewsFunctionsTestCase(TestCase):
    """TestCase for providing team_views_functions util testing."""

    def setUp(self):
        """Method that set ups basic constants before testing team_views_functions features."""

        first_user = CustomUser(id=20,
                                email='email@email.com')
        first_user.set_password('1111')
        first_user.save()

        second_user = CustomUser(id=200,
                                 email='tets@email.com')
        second_user.set_password('0000')
        second_user.save()

    def test_find_users_by_id_success(self):
        """Method that tests succeeded `find_users` method."""

        actual_members_list = team_views_functions.find_users([20])

        member = CustomUser.objects.get(id=20)
        expect_members_list = [member]

        self.assertListEqual(actual_members_list, expect_members_list)

    def test_find_users_by_id_not_success(self):
        """Method that tests unsucceeded `find_users` method."""

        actual_members_list = team_views_functions.find_users([25])

        self.assertIsNone(actual_members_list)

    def test_create_team_dict_success(self):
        """Method that tests succeeded `create_team_dict` method."""

        user = CustomUser.objects.get(id=20)
        data = {
            'name': 'name',
            'description': 'description',
            'image': 'link',
            'owner': 20,
            'members': [20]
        }

        expect_team_dict = {
            'owner': user,
            'members': [user],
            'name': 'name',
            'description': 'description',
            'image': 'link'
        }

        team_dict = team_views_functions.create_team_dict(data, user)

        self.assertDictEqual(team_dict, expect_team_dict)

    def test_create_team_dict_not_success_value_list_of_int_validator(self):
        """Method that tests unsucceeded `create_team_dict` method if value members_id not valid"""

        user = CustomUser.objects.get(id=20)
        data = {
            'name': 'name',
            'description': 'description',
            'image': 'link',
            'owner_id': 20,
            'members_id': ['not int']
        }

        team_dict = team_views_functions.create_team_dict(data, user)

        self.assertIsNone(team_dict)

    def test_create_team_dict_not_success_if_not_members(self):
        """Method that tests unsucceeded `create_team_dict` method if members_id not exist"""

        user = CustomUser.objects.get(id=20)
        data = {
            'name': 'name',
            'description': 'description',
            'image': 'link',
            'owner': 20,
            'members_id': [340]
        }

        team_dict = team_views_functions.create_team_dict(data, user)

        self.assertIsNone(team_dict)

    def test_get_users_to_add_members_success(self):
        """Method that tests succeeded `get_users` method."""

        user = CustomUser.objects.get(id=20)
        members_add = CustomUser.objects.get(id=200)

        data = {
            'owner_id': 20,
            'members_id_add': [200],
            'members_id_del': []
        }

        expect_tuple = (user, None, [members_add])

        get_users_tuple = team_views_functions.get_users(data, user)

        self.assertTupleEqual(get_users_tuple, expect_tuple)

    def test_get_users_not_add_members_id_add_is_empty(self):
        """Method that tests unsucceeded `get_users` method members_id_add empty"""

        user = CustomUser.objects.get(id=20)
        data = {
            'owner_id': 20,
            'members_id_add': [],
            'members_id_del': []
        }

        expect_tuple = (user, None, None)

        get_users_tuple = team_views_functions.get_users(data, user)

        self.assertTupleEqual(get_users_tuple, expect_tuple)

    def test_get_users_not_add_member_owner_get_bad_value(self):
        """Method that tests unsucceeded `get_users` method if members_id not exist"""

        user = CustomUser.objects.get(id=20)
        data = {
            'owner_id': 'owner',
            'members_id_add': [],
            'members_id_del': []
        }

        expect_tuple = (None, None, None)

        get_users_tuple = team_views_functions.get_users(data, user)

        self.assertTupleEqual(get_users_tuple, expect_tuple)

    def test_get_users_not_add_member_members_id_add_bad_value(self):
        """Method that tests unsucceeded `get_users` method if members_id_add take bad value"""

        user = CustomUser.objects.get(id=20)
        data = {
            'owner_id': 20,
            'members_id_add': ['not int'],
            'members_id_del': []
        }

        get_users_tuple = team_views_functions.get_users(data, user)

        self.assertIsNone(get_users_tuple)

    def test_get_users_add_member_not_success_member_not_in_list(self):
        """Method that tests unsucceeded `get_users` method if member not in list"""

        user = CustomUser.objects.get(id=20)
        data = {
            'owner_id': 20,
            'members_id_add': [210],
            'members_id_del': []
        }

        get_users_tuple = team_views_functions.get_users(data, user)

        self.assertIsNone(get_users_tuple)

    def test_get_users_add_member_not_success_member_get_bad_value(self):
        """Method that tests unsucceeded `get_users` method if member get bad value"""

        user = CustomUser.objects.get(id=20)
        data = {
            'owner_id': 20,
            'members_id_add': ['not int'],
            'members_id_del': []
        }

        get_users_tuple = team_views_functions.get_users(data, user)

        self.assertIsNone(get_users_tuple)

    def test_get_users_delete_members_success(self):
        """Method that tests success `get_users` members delete"""

        user = CustomUser.objects.get(id=20)
        members_del = CustomUser.objects.get(id=200)
        data = {
            'owner_id': 20,
            'members_id_add': [],
            'members_id_del': [200]
        }

        expect_tuple = (user, [members_del], None)

        get_users_tuple = team_views_functions.get_users(data, user)

        self.assertTupleEqual(get_users_tuple, expect_tuple)

    def test_get_users_delete_members_not_success_member_not_in_list(self):
        """Method that tests unsucceeded `get_users` method if members not in list"""

        user = CustomUser.objects.get(id=20)
        data = {
            'owner_id': 20,
            'members_id_add': [],
            'members_id_del': [201]
        }

        get_users_tuple = team_views_functions.get_users(data, user)

        self.assertIsNone(get_users_tuple)

    def test_get_users_delete_members_not_success_member_is_user(self):
        """Method that tests unsucceeded `get_users` method if member is user"""

        user = CustomUser.objects.get(id=20)
        data = {
            'owner_id': 20,
            'members_id_add': [],
            'members_id_del': [20]
        }

        get_users_tuple = team_views_functions.get_users(data, user)

        self.assertIsNone(get_users_tuple)

    def test_get_users_delete_members_not_success_members_id_del_bad_value(self):
        """Method that tests unsucceeded `get_users` method if members_id_del have bad value"""

        user = CustomUser.objects.get(id=20)
        data = {
            'owner_id': 20,
            'members_id_add': [],
            'members_id_del': ['not int']
        }

        get_users_tuple = team_views_functions.get_users(data, user)

        self.assertIsNone(get_users_tuple)

    def test_update_team_dict_success(self):
        """Method that tests success `update_team_dict` method"""

        user = CustomUser.objects.get(id=20)
        member = CustomUser.objects.get(id=200)
        data = {
            'name': 'name',
            'description': 'description',
            'image': 'link',
            'owner_id': 20,
            'members_id_add': [200],
            'members_id_del': []
        }

        expect_dict = {
            'description': 'description',
            'image': 'link',
            'members_add': [member],
            'members_del': None,
            'name': 'name',
            'owner': user
        }

        team_update_dict = team_views_functions.update_team_dict(data, user)

        self.assertDictEqual(team_update_dict, expect_dict)

    def test_update_team_dict_not_success_image_not_str(self):
        """Method that tests unsucceeded `update_team_dict` method bad image source"""

        user = CustomUser.objects.get(id=20)
        data = {
            'name': 'name',
            'description': 'description',
            'image': 1234,
            'owner_id': 20,
            'members_id_add': [],
            'members_id_del': []
        }

        team_update_dict = team_views_functions.update_team_dict(data, user)

        self.assertIsNone(team_update_dict)

    def test_update_team_dict_not_success_users_return_none(self):
        """Method that tests unsucceeded `update_team_dict` method when get_users return None"""

        user = CustomUser.objects.get(id=20)
        data = {
            'name': 'name',
            'description': 'description',
            'image': 'link',
            'owner_id': 20,
            'members_id_add': ['not int'],
            'members_id_del': []
        }

        team_update_dict = team_views_functions.update_team_dict(data, user)

        self.assertIsNone(team_update_dict)
