from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Competition, Match, Usage, User, Player, Coach, LeagueAdmin, Team

# Add Custom Admin Classes

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'username', 'email', 'role', 'password')
        }),
    )
    list_display = ('username', 'role', 'email', 'last_login', 'last_logout', 'is_staff')

# Register your models here.

admin.site.register(User, CustomUserAdmin)
admin.site.register(Player)
admin.site.register(Coach)
admin.site.register(LeagueAdmin)
admin.site.register(Team)
admin.site.register(Competition)
admin.site.register(Match)
admin.site.register(Usage)