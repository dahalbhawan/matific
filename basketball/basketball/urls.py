"""basketball URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from base import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'auth', views.AuthViewSet, basename='auth')
router.register(r'usage', views.UsageViewSet, basename='usage')
router.register(r'players', views.PlayerViewSet, basename='player')
router.register(r'coaches', views.CoachViewSet, basename='coach')
router.register(r'league-admins', views.LeagueAdminViewSet, basename='league-admin')
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'competitions', views.CompetitionViewSet, basename='competition')
router.register(r'matches', views.MatchViewSet, basename='match')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
