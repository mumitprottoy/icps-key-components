
def create_club_txt_files():
    from control.models import Club
    cd = 'operations/clubs/'
    file=open(cd+'clubs.txt', 'a')
    for club in Club.objects.all():
        data = f"{club.name},{club.acronym},{club.short_name},{club.logo_url}"
        file.write(data+'\n')
    file.close()


if __name__=='__main__': create_club_txt_files()