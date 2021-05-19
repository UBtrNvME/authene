"""Abstract class that describes behavior that all use cases should follow."""
from abc import ABC, abstractmethod


class UseCase(ABC):
    """
    Use case class that executes some actions that service exposes.

    Name of the use case should be self explanatory.
    Should preferably perform one action.
    """

    @abstractmethod
    def execute(self):
        """Execute action that use case encapsulates."""
