class CustomException(Exception):
    pass


class ManagerFromAnotherClub(CustomException):
    message = 'Player from another club cannot be a manager of this club'
    def __init__(self) -> None:
        super().__init__(self.message)


class SameClubMatch(CustomException):
    message = 'A club cannot play againts themselves.'
    def __init__(self) -> None:
        super().__init__(self.message)


class SamePlayerMultipleClub(CustomException):
    message = 'Already a player of a different club.'
    def __init__(self) -> None:
        super().__init__(self.message) 


class InvalidPlayer(CustomException):
    message = 'Invalid Player'
    def __init__(self) -> None:
        super().__init__(self.message)