"""
This module contains MS SQL Server specific logic that works with the BCP command line utility
"""
import subprocess

from bcp import Connection
from bcp.exceptions import DriverNotSupportedException
from bcp.core import BCPLoad, BCPDump
from ..files import LogFile, ErrorFile, DataFile


class MSSQLBCP:
    """This mixin provides utility functions for MSSQL's BCP. It serves as a mixin for BCPLoad and BCPDump subclasses
    """
    file = None
    batch_size = None

    def execute(self) -> subprocess.CompletedProcess:
        """This will run the instance's command via the BCP utility

        Returns: the result of the command line execution
        """
        return subprocess.run(f'bcp {self.command}', check=True)

    @property
    def command(self) -> str:
        raise NotImplementedError

    @property
    def config(self) -> str:
        """This method will generate a configuration string. It supports the delimiter and batch size options.

        Returns: a BCP formatted configuration string
        """
        config = f'-c -t "{self.file.delimiter}"'
        if self.batch_size is not None:
            config = f'{config} -b {self.batch_size}'
        return config

    @property
    def logging(self) -> str:
        """This method will generate a log file input string that will write the log file to the userprofile directory

        Returns: a BCP formatted log file string
        """
        log_file = LogFile()
        return f'-o "{log_file.path}"'

    @property
    def error(self) -> str:
        """This method will generate an error file input string that will write the error file to the userprofile directory

        Returns: a BCP formatted error file string
        """
        error_file = ErrorFile()
        return f'-e "{error_file.path}"'


class MSSQLLoad(MSSQLBCP, BCPLoad):
    """This class is the MS SQL Server implementation of the BCP Dump operation.

    Args:
        connection: the (mssql) Connection object that points to the database from which we want to export data
    """
    def __init__(self, connection: Connection, file: DataFile, table: str):
        if connection.driver != 'mssql':
            raise DriverNotSupportedException
        super().__init__(connection, file, table)
        self.batch_size = 10000

    @property
    def command(self) -> str:
        """This method will build the command that will export data from the supplied query and to the supplied file.
        It subs out all of the logic to the MSSQLBCP mixin.

        Args:
            input_file: the file whose data should be imported into the target database
            table: the into which the data will be written
        """
        return f'{self.table} in "{self.file.path}" {self.connection} {self.config} {self.logging} {self.error}'


class MSSQLDump(MSSQLBCP, BCPDump):
    """This class is the MS SQL Server implementation of the BCP Dump operation.

    Args:
        connection: the (mssql) Connection object that points to the database from which we want to export data
    """
    def __init__(self, connection: Connection, query: str, file: DataFile):
        if connection.driver != 'mssql':
            raise DriverNotSupportedException
        super().__init__(connection, query, file)

    @property
    def command(self) -> str:
        """This method will build the command that will export data from the supplied query and to the supplied file.
        It subs out all of the logic to the MSSQLBCP mixin.

        Args:
            query: the query defining the data to be exported
            output_file: the file to which the data will be written
        """
        return f'{self.query} queryout "{self.file.path}" {self.connection} {self.config} {self.logging}'
