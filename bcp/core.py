"""
This is the core module of the package, containing the core object. Along with Connection, it serves as an entry point
to the functionality of the bcp package.

Load:
This module contains the primary logic for importing data from a database. There is an abstract base class that serves
as a shell to specify required methods. Otherwise, there are driver specific subclasses that implement this abstract
base class along with methods pulled from the driver's mixin.

Dump:
This module contains the primary logic for exporting data from a database. There is an abstract base class that serves
as a shell to specify required methods. Otherwise, there are driver specific subclasses that implement this abstract
base class along with methods pulled from the driver's mixin.
"""

import abc
import subprocess

from .connections import Connection
from .files import DataFile
from .dialects import mssql
from .exceptions import DriverNotSupportedException


class BCP:
    """This is an interface over database-specific classes that provides generic methods to load/dump data to/from a
     database.

    Args:
        connection: a Connection object that contains authorization details and database details

    .. example::
        from bcp import BCP, Connection, DataFile

        conn = Connection('host', 'mssql', 'username', 'password')
        my_bcp = BCP(conn)
    """

    def __init__(self, connection: Connection):
        self.connection = connection

    def load(self, input_file: DataFile, table: str) -> subprocess.CompletedProcess:
        """This method provides an interface between the agnostic BCP class and the lower level database-specific BCP class

        Args:
            input_file: the file to be loaded into the database
            table: the table in which to land the data

        Returns: the return code from the command line

        .. example::
            from bcp import BCP, Connection, DataFile

            conn = Connection('host', 'mssql', 'username', 'password')
            my_bcp = BCP(conn)
            file = DataFile('pathtofile.csv')
            my_bcp.load(file, 'my_schema.my_table')
        """
        if self.connection.driver == 'mssql':
            loader = mssql.MSSQLLoad(self.connection, input_file, table)
        else:
            raise DriverNotSupportedException
        return loader.execute()

    def dump(self, query: str, output_file: DataFile) -> subprocess.CompletedProcess:
        """This method provides an interface between the agnostic BCP class and the lower level database-specific BCP class

        Args:
            query: the query whose results should be saved off to a file
            output_file: the file to which the results should be saved

        Returns: the return code from the command line

        .. example::
            from bcp import BCP, Connection, DataFile

            conn = Connection('host', 'mssql', 'username', 'password')
            my_bcp = BCP(conn)
            file = DataFile('pathtofile.csv')
            my_bcp.dump('select * from sys.tables', file)
        """
        if self.connection.driver == 'mssql':
            dumper = mssql.MSSQLDump(self.connection, query, output_file)
        else:
            raise DriverNotSupportedException
        return dumper.execute()


class BCPLoad(abc.ABC):
    """This is the abstract base class for all driver specific Dump implementations. It contains required methods and
    default values for all subclasses.

    Args:
        connection: the Connection object that points to the database from which we want to export data
    """

    def __init__(self, connection: Connection, file: DataFile, table: str):
        self.connection = connection
        self.file = file
        self.table = table

    @abc.abstractmethod
    def execute(self) -> subprocess.CompletedProcess:
        """This is the main entry point of the class

        Args:
            input_file: the file containing the data to be imported
            table: the table to which the data should be loaded

        Returns: the result of the bcp command from the shell
        """
        raise NotImplementedError


class BCPDump(abc.ABC):
    """This is the abstract base class for all driver specific Dump implementations. It contains required methods and
    default values for all subclasses.

    Args:
        connection: the Connection object that points to the database from which we want to export data
    """

    def __init__(self, connection: Connection, query: str, file: DataFile):
        self.connection = connection
        self.query = query
        self.file = file

    @abc.abstractmethod
    def execute(self) -> subprocess.CompletedProcess:
        """This is the main entry point of the class

        Args:
            query: the query to be executed against the database
            output_file: the file path to the file where the query results should be stored

        Returns: the result of the bcp command from the shell
        """
        raise NotImplementedError
