"""
This module contains the primary logic for exporting data from a database. There is an abstract base class that serves
as a shell to specify required methods. Otherwise, there are driver specific subclasses that implement this abstract
base class along with methods pulled from the driver's mixin.
"""
import subprocess
import pathlib
import abc
from .connection import Connection
from .exceptions import DriverNotSupportedException
from .sql_server import MSSQLBCP


class BCPDump(abc.ABC):
    """This is the abstract base class for all driver specific Dump implementations. It contains required methods and
    default values for all subclasses.

    Args:
        connection: the Connection object that points to the database from which we want to export data
    """

    def __init__(self, connection: Connection):
        self.connection = connection
        self.delimiter = '\t'
        self.batch_size = None

    @abc.abstractmethod
    def dump(self, query: str, output_file: pathlib.Path) -> subprocess.CompletedProcess:
        """This is the main entry point of the class

        Args:
            query: the query to be executed against the database
            output_file: the file path to the file where the query results should be stored

        Returns: the result of the bcp command from the shell
        """


class MSSQLDump(BCPDump, MSSQLBCP):
    """This class is the MS SQL Server implementation of the BCP Dump operation.

    Args:
        connection: the (mssql) Connection object that points to the database from which we want to export data
    """

    def __init__(self, connection: Connection):
        if connection.driver != 'mssql':
            raise DriverNotSupportedException
        super().__init__(connection)

    def dump(self, query: str, output_file: pathlib.Path) -> subprocess.CompletedProcess:
        """This is the main entry point of the class

        Args:
            query: the query to be executed against the database
            output_file: the file path to the file where the query results should be stored
        Returns: the result of the bcp command from the shell
        """
        self._build_command(query, output_file)
        return super()._run_command()

    def _build_command(self, query: str, output_file: pathlib.Path):
        """This method will build the command that will export data from the supplied query and to the supplied file.
        It subs out all of the logic to the MSSQLBCP mixin.

        Args:
            query: the query defining the data to be exported
            output_file: the file to which the data will be written
        """
        query = self._get_query_string(query)
        data_file = self._get_output_file_string(output_file)
        connection = self._get_connection_string()
        config = self._get_config_string()
        logging = self._get_logging_string()
        self.command = f'{query} {data_file} {connection} {config} {logging}'

