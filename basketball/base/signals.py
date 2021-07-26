from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.conf.global_settings import TIME_ZONE
from django.contrib.auth import get_user_model
from .models import Player, Coach, LeagueAdmin, Usage
from rest_framework.authtoken.models import Token

User = get_user_model()
# Signal receiver to create Player, Coach or LeagueAdmin instance, whichever appropriate, as User instance is created is created
def role_created(sender, instance, **kwargs):
    if instance.role == 1:
        Player.objects.get_or_create(user=instance)
    elif instance.role == 2:
        Coach.objects.get_or_create(user=instance)
    elif instance.role == 3:
        LeagueAdmin.objects.get_or_create(user=instance)
    else:
        pass

post_save.connect(receiver=role_created, sender=User)


# Signal to automatically trigger Token creation when User instance is created
def create_auth_token(sender, instance, **kwargs):
    Token.objects.get_or_create(user=instance)

post_save.connect(receiver=create_auth_token, sender=User)


# Signal to update usage statistics (login_times) upon user login
def update_login_times(sender, user, **kwargs):
    try:
        usage, created = Usage.objects.get_or_create(user=user)
        usage.login_times += 1
        usage.save()
    except Usage.DoesNotExist:
        pass

user_logged_in.connect(receiver=update_login_times)


# Signal to update usage statictics (usage_time) upon user logout
def update_usage_time(sender, user, **kwargs):
    try:
        usage, created = Usage.objects.get_or_create(user=user)
        user.last_logout = timezone.now()
        user.save()
        recent_usage = -(user.last_login - user.last_logout).total_seconds()/3600   #recent usage duration in hours
        print(user.last_logout)
        usage.usage_time += recent_usage
        usage.save()
    except Usage.DoesNotExist:
        pass

user_logged_out.connect(receiver=update_usage_time)