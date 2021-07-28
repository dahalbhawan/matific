from django.db import models

class PlayerQuerySet(models.QuerySet):
    
    def filter_by_team(self, team_id):
        return self.filter(team__id=team_id)
    
    # number of players in a team is 10, however if the number increases in future, the method can play a role.
    def count_by_team(self, team_id):
        return self.filter_by_team(team_id=team_id).count()

    def ninty_percentile(self, team_id):
        ninty_percentile_index = int(round(0.9*self.count_by_team(team_id=team_id)))
        return self.filter_by_team(team_id=team_id).order_by('-average_score')[ninty_percentile_index:]