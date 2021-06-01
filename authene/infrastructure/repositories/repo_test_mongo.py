from pymongo import MongoClient
from pymongo.collection import Collection
import hashlib


class User:
    def __init__(self, entity_id, username, password):
        self.__id = entity_id
        self.username = username
        self.password = password

    def __eq__(self, other):
        return self.__id == other.__id

    @property
    def id(self):
        return self.__id

    @classmethod
    def create_user(cls, username, password):
        entity_id = f"user:{username[0].lower()}{hashlib.sha1(username.encode('utf-8')).hexdigest()}"
        return User(entity_id=entity_id, username=username, password=password)


class Repository:
    def __init__(self, users: Collection):
        self.__users = users

    def __contains__(self, item):
        items = map(self._unmarshal, self.__users.find())
        while items:
            try:
                if item == next(items):
                    return True
            except StopIteration:
                break
        return False

    def add(self, user):
        self.__users.insert_one(self._marshal(user))

    def remove(self, username):
        return self.__users.delete_one({"username": username})

    def _marshal(self, user: User):
        return {"_id": user.id, "username": user.username, "password": user.password}

    def _unmarshal(self, document):
        document["entity_id"] = document.pop("_id")
        return User(**document)


class UnitOfWork:
    repo: Repository

    def __init__(self, repo):
        self.repo = repo

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    def commit(self):
        pass

    def rollback(self):
        pass
