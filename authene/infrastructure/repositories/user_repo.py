from authene.auth.domain.user import Repository
from authene.auth.domain.username import Username


class InMemoryRepository(Repository):
    def __init__(self):
        self.__users = []

    def find_by_username(self, username):
        username = Username(username)
        it = iter(self.__users)
        while self.__users:
            try:
                val = next(it)
                if val.username == username:
                    return val
            except StopIteration:
                break
        return None

    def all_users_lazy(self):
        for user in self.__users:
            yield user

    def all_users(self):
        return list(self.all_users_lazy())

    def add(self, user):
        self.__users.append(user)
