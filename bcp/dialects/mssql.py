"""
This module contains MS SQL Server specific logic that works with the BCP command line utility. None of these classes
are relevant beyond the scope of this library, and should not be used outside of the library.
"""
import subprocess

from ..exceptions import DriverNotSupportedException
from ..connections import Connection
from ..files import LogFile, ErrorFile, DataFile
from .base import BCPLoad, BCPDump


class MSSQLBCP:
    """This mixin provides properties for MSSQL's BCP. It serves as a mixin for BCPLoad and BCPDump subclasses below."""
    file = None
    batch_size = None

    @property
    def command(self) -> str:
        """
        This allows you to see the command that will be executed via bcp without executing the command, similar to
        how sqlalchemy can show you the generated query or execute the generated query. This makes debugging a little
        easier.

        Returns:
             the command that will be passed into the bcp command line utility
        """
        raise NotImplementedError

    @property
    def config(self) -> str:
        """
        This method will generate a configuration string. It supports the delimiter option.

        Returns:
             a BCP formatted configuration string
        """
        return f'-c -t "{self.file.delimiter}"'

    @property
    def logging(self) -> str:
        """
        This method will generate a log file string that will write the log file to the BCP_LOGGING_DIR directory.

        Returns:
             a BCP formatted log file string
        """
        log_file = LogFile()
        return f'-o "{log_file.path}"'


class MSSQLLoad(MSSQLBCP, BCPLoad):
    """
    This class is the MS SQL Server implementation of the BCP Load operation.

    Args:
        connection: the (mssql) Connection object that points to the database from which we want to export data
        file: the file whose data should be imported into the target database
        table: the into which the data will be written
    """
    def __init__(self, connection: Connection, file: DataFile, table: str):
        if connection.driver != 'mssql':
            raise DriverNotSupportedException
        super().__init__(connection, file, table)
        self.batch_size = 10000

    def execute(self) -> str:
        """
        This will run the instance's command via the BCP utility

        Returns:
             the name of the table that contains the data
        """
        subprocess.run(f'bcp {self.command}', check=True)
        return self.table

    @property
    def command(self) -> str:
        """
        This method will build the command that will import data from the supplied file to the supplied table.

        Returns:
             the command that will be passed into the BCP command line utility
        """
        return f'{self.table} in "{self.file.path}" {self.connection} {self.config} {self.logging} {self.error}'

    @property
    def config(self) -> str:
        """
        This method will generate a configuration string. It supports the delimiter and batch size options.

        Returns:
             a BCP formatted configuration string
        """
        return f'{super().config} -b {self.batch_size}'

    @property
    def error(self) -> str:
        """
        This method will generate an error file string that will write the error file to the BCP_DATA_DIR directory.

        Returns:
             a BCP formatted error file string
        """
        error_file = ErrorFile()
        return f'-e "{error_file.path}"'


class MSSQLDump(MSSQLBCP, BCPDump):
    """
    This class is the MS SQL Server implementation of the BCP Dump operation.

    Args:
        connection: the Connection object that points to the database from which we want to export data
        query: the query defining the data to be exported
        file: the file to which the data will be written
    """
    def __init__(self, connection: Connection, query: str, file: DataFile = None):
        if connection.driver != 'mssql':
            raise DriverNotSupportedException
        super().__init__(connection, query, file)

    def execute(self) -> DataFile:
        """
        This will run the instance's command via the BCP utility

        Returns:
             the data file object that contains the exported data
        """
        subprocess.run(f'bcp {self.command}', check=True)
        return self.file

    @property
    def command(self) -> str:
        """
        This method will build the command that will export data from the supplied table to the supplied file.

        Returns:
             the command that will be passed into the BCP command line utility
        """
        return f'"{self.query}" queryout "{self.file.path}" {self.connection} {self.config} {self.logging}'
