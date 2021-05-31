import itertools
from abc import ABCMeta, abstractmethod

from .events import DomainEvent


class Entity(metaclass=ABCMeta):
    """The base class of all entities."""

    _instance_id_generator = itertools.count()

    class Created(DomainEvent):
        pass

    class Discarded(DomainEvent):
        pass

    @abstractmethod
    def __init__(self, entity_id, entity_version):
        self.__id = entity_id
        self.__version = entity_version
        self.__discarded = False
        self.__instance_id = next(Entity._instance_id_generator)

    def _increment_version(self):
        self.__version += 1

    @property
    def instance_id(self):
        """A value unique among instances of this entity."""
        return self.__instance_id

    @property
    def id(self):
        """A string unique identifier for the entity."""
        self._check_not_discarded()
        return self.__id

    @property
    def version(self):
        """An integer version for the entity."""
        self._check_not_discarded()
        return self.__version

    @property
    def discarded(self):
        """True if this entity marked as discarded, otherwise False."""
        return self.__discarded

    def _check_not_discarded(self):
        if self.__discarded:
            raise DiscardedEntityError("Attempt to use {}".format(repr(self)))


class DiscardedEntityError(Exception):
    """Raised when an attempt is made to use a discarded Entity."""

    pass
