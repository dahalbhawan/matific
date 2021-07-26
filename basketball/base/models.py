from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    PLAYER, COACH, LEAGUE_ADMIN = 1, 2, 3
    USER_ROLE_CHOICES= (
      (PLAYER, 'Player'),
      (COACH, 'Coach'),
      (LEAGUE_ADMIN, 'League Admin'),
    )
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    role = models.IntegerField(choices=USER_ROLE_CHOICES, blank=True, null=True)
    last_logout = models.DateTimeField(blank=True, null=True)


class Usage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login_times = models.PositiveIntegerField(default=0, blank=True, null=True)
    usage_time = models.FloatField(default=0, blank=True, null=True)


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    average_score = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    number_of_caps = models.IntegerField(blank=True, null=True)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, blank=True, null=True)


class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Coaches'


class LeagueAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    coach = models.OneToOneField(Coach, on_delete=models.SET_NULL, blank=True, null=True)
    average_score = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)    


class Competition(models.Model):
    QUALIFIER, QUARTER_FINAL, SEMI_FINAL, FINAL = 1, 2, 3, 4
    TYPE_CHOICES = (
        (QUALIFIER, 'Qualifier'),
        (QUARTER_FINAL, 'Quarter Final'),
        (SEMI_FINAL, 'Semi Final'),
        (FINAL, 'Final'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES, blank=False, null=False)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)


class Match(models.Model):
    FIRST, SECOND = 1, 2
    WINNER_CHOICES = (
        (FIRST, 'First Team'),
        (SECOND, 'Second Team'),
    )
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, blank=True, null=True)
    venue = models.CharField(max_length=100, blank=True, null=True)
    first_team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True, related_name='first_team_matches')
    second_team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True, related_name='second_team_matches')
    winner = models.IntegerField(choices= WINNER_CHOICES)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Matches'
