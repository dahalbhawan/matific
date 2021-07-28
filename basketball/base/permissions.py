from rest_framework.permissions import BasePermission, SAFE_METHODS


# Add custom permissions here

# Custom permission class for allowing all kinds of authenticated users to utilize SAFE_METHODS (list, retrieve)
class CustomBasePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated

# permission class that allows SAFE METHODS 
class AllowSafe(CustomBasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.method in SAFE_METHODS
    
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj) and request.method in SAFE_METHODS

# superuser should have all permissions regardless
class IsSuperUser(CustomBasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


# this permission class allows admins to perform anything
class IsLeagueAdmin(CustomBasePermission):
    def has_permission(self, request, view):
        try:
            return super().has_permission(request, view) and request.user.role==3
        except AttributeError:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            return super().has_object_permission(request, view, obj) and request.user.role==3
        except AttributeError:
            return False


class IsCoach(CustomBasePermission):
    def has_permission(self, request, view):
        try:
            return super().has_permission(request, view) and request.user.role==2
        except AttributeError:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            return super().has_object_permission(request, view, obj) and request.user.role==2
        except AttributeError:
            return False


class IsTeamCoach(IsCoach):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and view.action == 'fetch_90_percentile'

    def has_object_permission(self, request, view, obj):
        try:
            return super().has_object_permission(request, view, obj) and obj.coach == request.user.coach
        except AttributeError:
            return False    


class IsAuthorizedCoach(IsCoach):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and view.action == 'retrieve'

    def has_object_permission(self, request, view, obj):
        try:
            return super().has_object_permission(request, view, obj) and request.user==obj.user
        except:
            return False


class IsPlayersCoach(IsCoach):
    def has_permission(self, request, view):
        return super().has_permission(request ,view) and view.action == 'retrieve'

    def has_object_permission(self, request, view, obj):
        try:
            return super().has_object_permission(request, view, obj) and obj.team.coach.user == request.user
        except AttributeError:
            return False


class IsPlayer(CustomBasePermission):
    def has_permission(self, request, view):
        try:
            return super().has_permission(request, view) and request.user.role==1
        except AttributeError:
            return False

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj) and request.user.role==1


class IsAuthorizedUser(CustomBasePermission):
    def has_permission(self, request, view):
         return super().has_permission(request, view) and view.action == 'retrieve'
            
    def has_object_permission(self, request, view, obj):
        try:
            return super().has_object_permission(request, view, obj) and obj==request.user
        except AttributeError:
            return False


class IsAuthorizedPlayer(IsPlayer):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and view.action == 'retrieve'

    def has_object_permission(self, request, view, obj):
        try:
            return super().has_object_permission(request, view, obj) and obj.user==request.user
        except AttributeError:
            return False


class IsTeamPlayer(IsPlayer):
    def has_object_permission(self, request, view, obj):
        try:
            return super().has_object_permission(request, view, obj) and request.user in [player.user for player in obj.player_set.all()]
        except AttributeError:
            return False




