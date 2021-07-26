from .models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
import base64


class TestGetUsers(APITestCase):
    def test_unauthorized(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authorized(self):
        client = APIClient()
        user = User.objects.filter(username='leagueadmin')
        #league admin can view all users
        client.force_authenticate()
        # authorization = 'Basic ' + base64.b64encode(bytes('bhawan:artofwar', 'utf8')).decode('utf8')
        # client.credentials(HTTP_AUTHORIZATION = authorization)
        response = client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


