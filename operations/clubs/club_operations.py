from entities.models import Club, ClubGroup

def create_clubs():
    file = open('operations/clubs/clubs.txt', 'r')
    club_lines = file.read().split('\n')

    for c in club_lines:
        parts = c.split(',')
        group = ClubGroup.objects.get(name=parts[3])
        club = Club(
            name=parts[0],
            acronym=parts[1],
            short_name=parts[2],
            group=group,
            logo_url=parts[4]
        )
        club.save()
        print(club.name, 'is created.')


if __name__ == '__main__':
    create_clubs()
        
    
    
    
    