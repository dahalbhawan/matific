from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Coach, Competition, LeagueAdmin, Match, Player, Team, Usage, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'role', 'last_login', 'last_logout']

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserWithTokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'role', 'auth_token']
    
    def get_auth_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class EmptySerializer(serializers.Serializer):
    pass

class UsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usage
        fields = '__all__'
        depth = 1

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['user', 'height', 'average_score', 'number_of_caps', 'team']
        depth = 1
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.get('user').pop('password')
        response.get('user').pop('groups')
        response.get('user').pop('user_permissions')
        return response


class CoachSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Coach
        fields = ['user', 'team']
        depth = 1
    
    def get_team(self, obj):
        return obj.team.id
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.get('user').pop('password')
        response.get('user').pop('groups')
        response.get('user').pop('user_permissions')
        return response


class LeagueAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeagueAdmin
        fields = ['user']
        depth = 1
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.get('user').pop('password')
        response.get('user').pop('groups')
        response.get('user').pop('user_permissions')
        return response


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        depth = 2
    

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'
        depth = 1


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'
        depth = 1