from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Coach, Competition, LeagueAdmin, Match, Player, Usage, User, Team
from .serializers import *
from .utils.authentication import get_and_authenticate_user
from .permissions import AllowSafe, IsAuthorizedCoach, IsAuthorizedPlayer, IsAuthorizedUser, IsLeagueAdmin, IsLeagueAdmin, IsPlayersCoach, IsSuperUser, IsTeamCoach



# users details should not even be visible to SAFE METHODS so permission classes that block safe methods are used
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser | IsLeagueAdmin | IsAuthorizedUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = EmptySerializer
    serializer_classes = {
        'login': UserLoginSerializer,
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = UserWithTokenSerializer(user).data
        login(request, user)
        return Response(data=data, status=status.HTTP_200_OK)
    
    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'details': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)
    
    @action(methods=['GET', ], detail=False)
    def currentuser(self, request):
        user = request.user
        if user.is_authenticated:
            serializer=UserWithTokenSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'no user is authenticated'}, status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class UsageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLeagueAdmin | IsSuperUser]
    queryset = Usage.objects.all()
    serializer_class = UsageSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorizedPlayer | IsPlayersCoach | IsLeagueAdmin | IsSuperUser]
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class CoachViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthorizedCoach | IsLeagueAdmin | IsSuperUser]
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer


class LeagueAdminViewSet(viewsets.ModelViewSet):
    permission_classes=[IsLeagueAdmin | IsSuperUser]
    queryset = LeagueAdmin.objects.all()
    serializer_class = LeagueAdminSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsTeamCoach | IsLeagueAdmin | IsSuperUser]

    @action(methods=['GET'], detail=True, permission_classes=[IsTeamCoach])
    def fetch_90_percentile(self, request, pk=None):
        self.get_object()
        players = Player.objects.ninty_percentile(pk)
        data = PlayerSerializer(players, many=True).data
        return Response(data, status=status.HTTP_200_OK)
        

class CompetitionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLeagueAdmin | IsSuperUser | AllowSafe]
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


class MatchViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLeagueAdmin | IsSuperUser | AllowSafe]
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

