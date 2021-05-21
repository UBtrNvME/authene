"""
Database adapter abstraction that defines common interface for persistent data sources.

database connection string:
    schema://username:password@hostname:port/database_name?key=value
"""
from abc import ABC, abstractmethod


class DatabaseAdapter(ABC):
    """
    Database adapter abstraction, which has to be implemented with concrete classes.

    Should define common interface for SQL and NOSQL data sources.
    """

    def __init__(self, connection_string):
        """Initialise database adapter with database connection string."""
        parameters = self._parse_db_connection_string(connection_string)
        self.__db = self._connect(parameters)

    @abstractmethod
    def _parse_db_connection_string(self, connection_string):
        """Parse connection string to the dictionary format."""

    @abstractmethod
    def _connect(self, parameters):
        """Connect to the database and return database object."""

    # TODO:
    #   Here should be other database methods
    #   that will allow manipulation over data source.
