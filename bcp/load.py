"""
This module contains the primary logic for importing data from a database. There is an abstract base class that serves
as a shell to specify required methods. Otherwise, there are driver specific subclasses that implement this abstract
base class along with methods pulled from the driver's mixin.
"""
import subprocess
import pathlib
import abc
from .connection import Connection
from .exceptions import DriverNotSupportedException
from .sql_server import MSSQLBCP


class BCPLoad(abc.ABC):
    """This is the abstract base class for all driver specific Dump implementations. It contains required methods and
    default values for all subclasses.

    Args:
        connection: the Connection object that points to the database from which we want to export data
    """

    def __init__(self, connection: Connection):
        self.connection = connection
        self.delimiter = '\t'
        self.batch_size = 10000

    @abc.abstractmethod
    def load(self, input_file: pathlib.Path, table: str) -> subprocess.CompletedProcess:
        """This is the main entry point of the class

        Args:
            input_file: the file containing the data to be imported
            table: the table to which the data should be loaded

        Returns: the result of the bcp command from the shell
        """


class MSSQLLoad(BCPLoad, MSSQLBCP):
    """This class is the MS SQL Server implementation of the BCP Dump operation.

    Args:
        connection: the (mssql) Connection object that points to the database from which we want to export data
    """

    def __init__(self, connection: Connection):
        if connection.driver != 'mssql':
            raise DriverNotSupportedException
        super().__init__(connection)

    def load(self, input_file: pathlib.Path, table: str) -> subprocess.CompletedProcess:
        """This is the main entry point of the class

        Args:
            input_file: the file containing the data to be imported
            table: the table to which the data should be loaded

        Returns: the result of the bcp command from the shell
        """
        self._build_command(input_file, table)
        return super()._run_command()

    def _build_command(self, input_file: pathlib.Path, table: str):
        """This method will build the command that will export data from the supplied query and to the supplied file.
        It subs out all of the logic to the MSSQLBCP mixin.

        Args:
            input_file: the file whose data should be imported into the target database
            table: the into which the data will be written
        """
        data_file = self._get_input_file_string(input_file)
        connection = self._get_connection_string()
        config = self._get_config_string()
        logging = self._get_logging_string()
        error = self._get_error_string()
        self.command = f'{table} {data_file} {connection} {config} {logging} {error}'
