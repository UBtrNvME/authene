"""
Database adapter abstraction that defines common interface for persistent data sources.

database connection string:
    schema://username:password@hostname:port/database_name?key=value
"""
from abc import ABC, abstractmethod


class DBMSClient(ABC):
    """
    Database Management System Client Abstraction.

    Which has to be implemented with concrete classes.
    Should define common interface for SQL and NOSQL data sources.
    """

    def __init__(self, connection_string):
        """Initialise database adapter with database connection string."""
        parameters = self._parse_db_connection_string(connection_string)
        self.__client = self._connect(parameters)
        self.__databases = {}

    @abstractmethod
    def _parse_db_connection_string(self, connection_string):
        """Parse connection string to the dictionary format."""

    @abstractmethod
    def _connect(self, parameters):
        """Connect to the database and return database object."""

    @abstractmethod
    def create_database(self, name) -> "Database":
        """Create database."""

    @abstractmethod
    def drop_database(self, name) -> bool:
        """Drop database."""


class Database(ABC):
    """Abstraction over database object."""

    def __init__(self, client, name):
        self.name = name
        self.__tables = {}
        self.__client = client

    @abstractmethod
    def create_table(self, table_name, schema) -> "Table":
        """Create table in database with name equal table_name and schema."""

    @abstractmethod
    def drop_table(self, table_name) -> bool:
        """Drop table with table_name equal name."""

    def __getitem__(self, table_name) -> "Table":
        if table_name in self.__tables:
            return self.__tables[table_name]
        # FIXME: Implement specific Error!
        raise KeyError(f"Table {table_name} doesn't exist")


class Table(ABC):
    """Abstraction over Table/Collection object."""

    def __init__(self, database, name):
        self.name = name
        self.__database = database

    @abstractmethod
    def add_one(self, data):
        """Add one object to the table."""

    @abstractmethod
    def update_one(self, a_filter, data):
        """Update one entity in table that match a filter with data."""

    @abstractmethod
    def get_one(self, a_filter):
        """Get one entity from the table that matches a_filter criteria."""

    @abstractmethod
    def delete_one(self, a_filter):
        """Delete one entity from the table that matches a_filter criteria."""
