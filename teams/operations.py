from control.models import Player

def get_available_kit_numbers(club):
    return [
        k for k in range(0,100) 
        if not Player.objects.filter(club=club, kit_number=k).exists()
    ]