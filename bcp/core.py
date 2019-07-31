"""
This is the core module of the package, containing the core object. Along with Connection, it serves as an entry point
to the functionality of the bcp package.
"""
import pathlib
import subprocess
from .connection import Connection
from .exceptions import DriverNotSupportedException
from . import load
from . import dump


class BCP:
    """This is the core object of the package. It provides methods to load/dump data to/from a database

    Args:
        connection: a connection object that contains authorization details and database details
    """

    def __init__(self, connection: Connection):
        self.connection = connection
        self._set_handlers()

    def load(self, input_file: pathlib.Path, table: str) -> subprocess.CompletedProcess:
        """This method provides an interface between the agnostic BCP class and the lower level database-specific BCP class

        Args:
            input_file: the file to be loaded into the database
            table: the table in which to land the data

        Returns: the return code from the command line
        """
        return self.bcp_load.load(input_file, table)

    def dump(self, query: str, output_file: pathlib.Path) -> subprocess.CompletedProcess:
        """This method provides an interface between the agnostic BCP class and the lower level database-specific BCP class

        Args:
            query: the query whose results should be saved off to a file
            output_file: the file to which the results should be saved

        Returns: the return code from the command line
        """
        return self.bcp_dump.dump(query, output_file)

    def _set_handlers(self):
        """This method assigns the lower level database-specific BCP classes and enforces driver selection."""
        if self.connection.driver == 'mssql':
            self.bcp_load = load.MSSQLLoad(self.connection)
            self.bcp_dump = dump.MSSQLDump(self.connection)
        else:
            raise DriverNotSupportedException
