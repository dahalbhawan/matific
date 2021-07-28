from ..models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

PASSWORD = 'artofwar'


#test case for List actions on User model
class TestListUsers(APITestCase):

    def setUp(self):
        self.url = '/users/'

        # create three roles. Their tokens will be autocreated.
        self.player = User.objects.create(username='player1', password=PASSWORD, role=1)
        self.coach = User.objects.create(username='coach1', password=PASSWORD, role=2)
        self.leagueadmin = User.objects.create(username='leagueadmin', password=PASSWORD, role=3)
        self.player_token = Token.objects.get(user=self.player)
        self.coach_token = Token.objects.get(user=self.coach)
        self.leagueadmin_token = Token.objects.get(user=self.leagueadmin)

        # create API Clients for three roles
        self.player_client, self.coach_client, self.leagueadmin_client = [APIClient()]*3

        # authenticate all clients with Token authentication
        self.player_client.credentials(HTTP_AUTHORIZATION = 'Basic ' + self.player_token.key)
        self.coach_client.credentials(HTTP_AUTHORIZATION = 'Basic' + self.coach_token.key)
        self.leagueadmin_client.credentials(HTTP_AUTHORIZATION = 'Basic ' + self.leagueadmin_token.key)

    # unauthenticated users should not be able to get any user details
    def test_unauthenticated(self):
        response = self.client.get(self.url) # using unauthenticated client
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # test authenticated but unauthorized user, player and coach roles cannot list users
    def test_unauthorized(self):
        # Bypass Basic auth (username and password authentication)
        self.player_client.force_authenticate(user=self.player)
        self.coach_client.force_authenticate(user=self.coach)

        response_for_player, response_for_coach = self.player_client.get(self.url), self.coach_client.get(self.url)
        self.assertEqual(response_for_player.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_for_coach.status_code, status.HTTP_403_FORBIDDEN)

    # test both authenticated and authorized role (leagueadmin)
    def test_authorized(self):
        # Bypass Basic auth (username and password authentication)
        self.leagueadmin_client.force_authenticate(user=self.leagueadmin)

        response_for_leagueadmin = self.leagueadmin_client.get(self.url)
        self.assertEqual(response_for_leagueadmin.status_code, status.HTTP_200_OK)


# Test case for Retrieve action on User model
class TestRetrieveUser(APITestCase):
    def setUp(self):
        self.url = '/users/{}/'
        
        # create three roles. Their tokens will be autocreated.
        self.player = User.objects.create(username='player1', password=PASSWORD, role=1)
        self.next_player = User.objects.create(username='player2', password=PASSWORD, role=1)
        self.coach = User.objects.create(username='coach1', password=PASSWORD, role=2)
        self.leagueadmin = User.objects.create(username='leagueadmin', password=PASSWORD, role=3)
        self.player_token = Token.objects.get(user=self.player)
        self.next_player_token = Token.objects.get(user=self.next_player)
        self.coach_token = Token.objects.get(user=self.coach)
        self.leagueadmin_token = Token.objects.get(user=self.leagueadmin)

        # create API Clients for three roles
        self.player_client, self.next_player_client, self.coach_client, self.leagueadmin_client = [APIClient()]*4

        # authenticate all clients with Token authentication
        self.player_client.credentials(HTTP_AUTHORIZATION = 'Basic ' + self.player_token.key)
        self.next_player_client.credentials(HTTP_AUTHORIZATION = 'Basic ' + self.next_player_token.key)
        self.coach_client.credentials(HTTP_AUTHORIZATION = 'Basic' + self.coach_token.key)
        self.leagueadmin_client.credentials(HTTP_AUTHORIZATION = 'Basic ' + self.leagueadmin_token.key)
    
    # unauthenticated users should not be able to get any user details
    def test_unauthenticated(self):
        response = self.client.get(self.url.format(1))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # coaches should not be able to retrieve user data directly from user's urls
    # other players should not be able to retrive user data except their own 
    def test_unauthorized(self):
        url = self.url.format(self.player.pk)

        self.next_player_client.force_authenticate(user=self.next_player)
        self.coach_client.force_authenticate(user=self.coach)

        response_for_next_player, response_for_coach = self.next_player_client.get(url), self.coach_client.get(url)

        self.assertEqual(response_for_next_player.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_for_coach.status_code, status.HTTP_403_FORBIDDEN)

    # test authennticated and authorized player.
    # players should be able to access own data
    # league admins should be able to retrieve any user data
    def test_authorized_user(self):
        url = self.url.format(self.player.pk)

        self.player_client.force_authenticate(user=self.player)
        self.leagueadmin_client.force_authenticate(user=self.leagueadmin)

        response_for_player, response_for_leagueadmin = self.player_client.get(url), self.player_client.get(url)

        self.assertEqual(response_for_player.status_code, status.HTTP_200_OK)
        self.assertEqual(response_for_leagueadmin.status_code, status.HTTP_200_OK)



