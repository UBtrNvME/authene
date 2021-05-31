class UsernameAlreadyInUse(Exception):
    def __init__(self, username):
        super().__init__(f"The username {username} is already in use")
