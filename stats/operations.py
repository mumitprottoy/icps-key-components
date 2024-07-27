from .models import MatchDay, Fixture
from control.models import Club, ClubGroup

def get_group_teams(group, Club):
    return [
        t for t in Club.objects.filter(group=group).all()
    ]


def get_group(group_name):
    return ClubGroup.objects.filter(name=group_name).first()

def create_matchPOV(teams, MPOV):
    for t in teams:
        for o in teams:
            if o!=t: MPOV(club=t, opponent=o).save()


def create_all_matchPOV(Group, Club, MPOV):
    for g in Group.objects.all():
        teams = get_group_teams(g, Club)
        create_matchPOV(teams, MPOV)
                


def sort_matches(a:list) -> list:
    for i in range(len(a)-1):
        k = a[i+1]
        while a[i].match_time.hour>k.match_time.hour and i>=0:
            a[i+1] = a[i]
            print(a)
            i-=1
        a[i+1] = k
    return a



def get_fixture():
    fixtures = list()
    for d in MatchDay.objects.all():
        if Fixture.objects.filter(match_day=d).exists():
            matches = [f for f in Fixture.objects.filter(match_day=d).all()]
            if len(matches)>=2: matches = sort_matches(matches)
            fixtures.append({
                'date':d.__str__(),
                'matches':matches
            })
    
    return fixtures
            

def get_every_other_matches():
    from control.models import ClubGroup
    group_teams = []
    for g in ClubGroup.objects.all():
        g_teams=[]
        for c in Club.objects.filter(group=g).all():
            pass 



def make_group_table(group_name):
    g = get_group(group_name)
    teams = get_group_teams(g, Club)
    group_table=list()
    for t in teams:
        pass
    
    
    