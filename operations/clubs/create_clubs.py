from control.models import Club, ClubGroup

file = open('operations/clubs/clubs.txt', 'r')
club_lines = file.read().split('\n')

for c in club_lines:
    parts = c.split(',')
    Club(
        name=parts[0],
        acronym=parts[1],
        short_name=parts[2],
        logo_url=parts[4]
    ).save()
    
    
    
    