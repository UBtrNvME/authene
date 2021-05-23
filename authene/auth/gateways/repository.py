"""
Repository abstract class that defines basic methods that all repositories should have.

Implementations of this interface should be Entity Driven!
"""
from abc import ABC, abstractmethod


class Repository(ABC):
    """Abstract repository class, that defines simple interface over persistent data."""

    def __init__(self, dbms_adapter):
        """
        Initialise Repository with database adapter provided.

        Classes that inherit from Abstract Repository should use interface provided by
        adapter class.
        """
        self.__adapter = dbms_adapter

    @abstractmethod
    def create(self, data):
        """Create new entry in storage using data."""

    @abstractmethod
    def get(self, **kwargs):
        """Get entry from persistent storage using unique identifier."""
