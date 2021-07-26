from random import randint, uniform
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from base.models import User, Usage, Player, Coach, LeagueAdmin, Team, Match, Competition

# Command to populate database tables with some arbritary data
class Command(BaseCommand):
    help = 'Create fake data'

    def _create_matches(self, competition_type=1, num_teams=16, past_winner_list=None):
        if past_winner_list == None:
            team_set = Team.objects.all()
        else:
            team_set = past_winner_list
        step = 2
        if num_teams//2 == 1:
            step == 1
        for i in range(0, num_teams//2, 1):
            Match.objects.create(
                competition=Competition.objects.get(type=competition_type),
                first_team=team_set[i],
                second_team=team_set[i+1],
                winner=randint(1, 2),
            )


    def handle(self, *args, **kwargs):
        PASSWORD = make_password('artofwar')

        # first create a superuser
        print("creating superuser ......")
        User.objects.create(
            username='bhawan', 
            email='dahalbhawan@gmail.com', 
            password=PASSWORD,
            is_staff=True,
            is_superuser=True
        )
        print("superuser created successfully.")

        # create a League Admin
        print("creating league admin ......")
        User.objects.create(
            username='leagueadmin',
            password=PASSWORD,
            role=3
        )
        print("league admin created successfully.")

        # create 16 Coaches
        print("creating coaches ......")
        for i in range(0, 16):
            User.objects.create(
                username=f'coach{i+1}', 
                password=PASSWORD, 
                role=2
            )
        print("coaches created successfully.")
        
        # create 160 Players
        print("creating players ......")
        for i in range(0, 160):
            User.objects.create(
                username=f'player{i+1}',
                password=PASSWORD,
                role=1
            )
        print("players created successfully.")

        # create 16 teams
        print("creating teams ......")
        for i in range(0, 16):
            Team.objects.create(
                name=f'Team{i+1}', 
                coach=Coach.objects.get(pk=i+1),
                average_score=round(uniform(20,30), 2)
            )
        print("teams created successfully.")

        # update the players to add additional features like height, average_score ...
        print("updating players details ......")
        counter=0
        for player in Player.objects.all():
            player.height = round(uniform(5.70, 6.50), 2)
            player.average_score = round(uniform(5.00, 10.00), 2)
            player.number_of_caps = randint(0, 100)
            player.team = Team.objects.get(pk=counter//10+1)
            player.save()
            counter += 1
        print("players details updated successfully.")

        # create 4 types of competitions
        print("creating competitions ......")
        for i in range(0, 4):
            Competition.objects.create(
                type=i+1,
            )
        print("competitions created successfully.")
        
        # create 8 matches for Round 1 competition
        print("creating qualifier matches ......")
        self._create_matches()
        print("qualifier matches created successfully.")

        # create 4 matches for Round 2 competition selecting the winners from Round 1
        print("creating second round matches ......")
        round1_matches = Match.objects.filter(competition=Competition.objects.get(type=1))
        round1_winners = [match.first_team if match.winner==1 else match.second_team for match in round1_matches]
        self._create_matches(competition_type=2, num_teams=8, past_winner_list=round1_winners)
        print("second round matches created successfully.")
        
        # create 2 matches for Round 3 competition selecting the winners from Round 2
        print("creating third round matches ......")
        round2_matches = Match.objects.filter(competition=Competition.objects.get(type=2))
        round2_winners = [match.first_team if match.winner==1 else match.second_team for match in round2_matches]
        self._create_matches(competition_type=3, num_teams=4, past_winner_list=round2_winners)
        print("third round matches created successfully.")

        # create 1 match for final competition (Round 4) selecting the winners from Round 3
        print("creating final match ......")
        round3_matches = Match.objects.filter(competition=Competition.objects.get(type=3))
        round3_winners = [match.first_team if match.winner==1 else match.second_team for match in round3_matches]
        self._create_matches(competition_type=4, num_teams=2, past_winner_list=round3_winners)
        print("final matche created successfully.")

        print("\nDatabase population completed successfully.\n--------------------------------")

    
