import json
from django.test import TestCase, Client
from authentication.models import CustomUser


class TestLoginRequiredTestCase(TestCase):

    def setUp(self):
        """
        Method that provides preparation before starting testing  custom JSON check
        and permitted paths for anonymous users
        """
        user = CustomUser.objects.create(id=12, email='someemail@gmail.com', is_active=True)
        user.set_password('1234')
        user.save()
        self.authenticated_client = Client()
        self.authenticated_client.login(email='someemail@gmail.com', password='1234')
        self.not_authenticated_data = {'email': 'mail@mail.co', 'password': '1234'}
        self.authenticated_data = {'email': 'someemail@gmail.com', 'password': '1234'}
        
    def test_put_path_notapi(self):
        """
        Method that tests response when path starts not with api
        """
        response = self.client.get("v1/user/")
        self.assertEqual(response.status_code, 404)

    def test_put_badencoded_data(self):
        """
        Method that tests response when data can't be decoded 
        """
        data = 'some data'
        response = self.client.post('/api/v1/',
                                    data, 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_notauthenticated_user_notalouded_path(self):
        """
        Method that tests response if request user is not authenticated but path is not from  ANONYMOUS_USERS_PATHS
        """
        response = self.client.post('/api/v1/', 
                                    json.dumps(self.not_authenticated_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_notauthenticated_user_foranon_path(self):
        """
        Method that tests response when user is not authenticated and path is from ANONYMOUS_USERS_PATHS
        """
        response = self.client.post('/api/v1/user/login/', 
                                    json.dumps(self.not_authenticated_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_authenticated_user_pathforanon(self):
        """
        Method that tests response when user is not authenticated and path is from ANONYMOUS_USERS_PATHS
        """
        response = self.authenticated_client.post('/api/v1/user/login/', 
                                                  json.dumps(self.authenticated_data),
                                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
    def test_authenticated_user_path_fornotanon(self):
        """
        Method that tests response when user is not authenticated and path is from ANONYMOUS_USERS_PATHS
        """
        response = self.authenticated_client.post('/api/v1/', 
                                                  json.dumps(self.authenticated_data), 
                                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
