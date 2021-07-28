from ..models import User, Team, Coach
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

PASSWORD = 'artofwar'

# Test case for List action on  Team model
class TestListTeam(APITestCase):

    def setUp(self):
        self.url = '/teams/'
        
        # create three roles. Their tokens will be autocreated.
        self.player = User.objects.create(username='player2', password=PASSWORD, role=1)
        self.coach = User.objects.create(username='coach1', password=PASSWORD, role=2)
        self.leagueadmin = User.objects.create(username='leagueadmin', password=PASSWORD, role=3)
        self.Team = Team.objects.create(name='Team1', coach=self.coach.coach)
        self.player_token = Token.objects.get(user=self.player)
        self.coach_token = Token.objects.get(user=self.coach)
        self.leagueadmin_token = Token.objects.get(user=self.leagueadmin)

        # create API Clients for three roles
        self.player_client, self.coach_client, self.leagueadmin_client = [APIClient()]*3
        
        # authenticate all clients with Token authentication
        self.player_client.credentials(HTTP_AUTHORIZATION = 'Basic ' + self.player_token.key)
        self.coach_client.credentials(HTTP_AUTHORIZATION = 'Basic' + self.coach_token.key)
        self.leagueadmin_client.credentials(HTTP_AUTHORIZATION = 'Basic ' + self.leagueadmin_token.key)

    # clients that do not have login credentials or token
    def test_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # None role than leagueadmin can list all teams
    def test_unauthorized(self):
        self.player_client.force_authenticate(user=self.player)
        self.coach_client.force_authenticate(user=self.coach)
        response_for_player, response_for_coach = self.player_client.get(self.url), self.coach_client.get(self.url)
        self.assertEqual(response_for_player.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_for_coach.status_code, status.HTTP_403_FORBIDDEN)

    #league admin can view all players
    def test_authorized(self):
        self.leagueadmin_client.force_authenticate(user=self.leagueadmin)
        response = self.leagueadmin_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# test case for Retrieve action on Team
class TestRetrieveTeam(APITestCase):
    def setUp(self):
        self.url = '/teams/{}/'
        
        # create two players, two coaches, two teams and a leagueadmin
        self.player1 = User.objects.create(username='player1', password=PASSWORD, role=1)
        self.player2 = User.objects.create(username='player2', password=PASSWORD, role=1)
        self.coach1 = User.objects.create(username='coach1', password=PASSWORD, role=2)
        self.coach2 = User.objects.create(username='coach2', password=PASSWORD, role=2) 
        self.leagueadmin = User.objects.create(username='leagueadmin', password=PASSWORD, role=3)

        # create two teams and assign coaches
        self.team1 = Team.objects.create(name='Team1', coach=self.coach1.coach)
        self.team2 = Team.objects.create(name='Team2', coach=self.coach2.coach)

        # add players to two different teams
        self.player1.team = self.team1
        self.player2.team = self.team2
        self.player1.save()
        self.player2.save()

        self.player1_token = Token.objects.get(user=self.player1)
        self.player2_token = Token.objects.get(user=self.player2)
        self.coach1_token = Token.objects.get(user=self.coach1)
        self.coach2_token = Token.objects.get(user=self.coach2)
        self.leagueadmin_token = Token.objects.get(user=self.leagueadmin)

        # create API Clients for three roles
        self.player1_client, self.player2_client, self.coach1_client, self.coach2_client, self.leagueadmin_client = [APIClient()]*5
        
        # authenticate all clients with Token authentication
        self.player1_client.credentials(HTTP_AUTHORIZATION = 'Basic ' + self.player1_token.key)
        self.player2_client.credentials(HTTP_AUTHORIZATION = 'Basic ' + self.player2_token.key)
        self.coach1_client.credentials(HTTP_AUTHORIZATION = 'Basic' + self.coach1_token.key)
        self.coach2_client.credentials(HTTP_AUTHORIZATION = 'Basic' + self.coach2_token.key)
        self.leagueadmin_client.credentials(HTTP_AUTHORIZATION = 'Basic ' + self.leagueadmin_token.key)

    # any players, coaches from other team are unauthorized to retrieve team info
    def test_unauthorized(self):
        url = self.url.format(self.team1.pk) 
        self.player1_client.force_authenticate(user=self.player1)
        self.player2_client.force_authenticate(user=self.player2)
        self.coach2_client.force_authenticate(user=self.coach2)
        response_for_player1 = self.player1_client.get(url)
        response_for_player2 = self.player2_client.get(url)
        response_for_coach2 = self.coach2_client.get(url)
        self.assertEqual(response_for_player1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_for_player2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_for_coach2.status_code, status.HTTP_403_FORBIDDEN)

    # league admin and same team coach can retrieve team info
    def test_authorized(self):
        url = self.url.format(self.team1.pk) 
        self.coach1_client.force_authenticate(user=self.coach1)
        self.leagueadmin_client.force_authenticate(user=self.leagueadmin)
        response_for_coach1 = self.coach1_client.get(url)
        response_for_leagueadmin = self.leagueadmin_client.get(url)
        self.assertEqual(response_for_coach1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_for_leagueadmin.status_code, status.HTTP_200_OK)


# test case to check if only corresponding coaches can retrieve players whose average score is in 90 percentile of all players average score
class Test90PercentilePlayers(TestRetrieveTeam):
    def setUp(self):
        super().setUp()
        self.url = self.url+'fetch_90_percentile/'
    
    # all others except corresponding team's coach are unauthorized
    def test_unauthorized(self):
        url = self.url.format(self.team1.pk) 
        self.player1_client.force_authenticate(user=self.player1)
        self.player2_client.force_authenticate(user=self.player2)
        self.coach2_client.force_authenticate(user=self.coach2)
        self.leagueadmin_client.force_authenticate(user=self.leagueadmin)
        response_for_player1 = self.player1_client.get(url)
        response_for_player2 = self.player2_client.get(url)
        response_for_coach2 = self.coach2_client.get(url)
        response_for_leagueadmin = self.leagueadmin_client.get(url)
        self.assertEqual(response_for_player1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_for_player2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_for_coach2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_for_leagueadmin.status_code, status.HTTP_403_FORBIDDEN)
    
    # league admin and same team coach can retrieve team info
    def test_authorized(self):
        url = self.url.format(self.team1.pk) 
        print(url)
        self.coach1_client.force_authenticate(user=self.coach1)
        response_for_coach1 = self.coach1_client.get(url)
        self.assertEqual(response_for_coach1.status_code, status.HTTP_200_OK)
