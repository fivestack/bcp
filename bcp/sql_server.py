"""
This module contains MS SQL Server specific logic that works with the BCP command line utility
"""
import pathlib
import subprocess
from .files import LogFile, ErrorFile


class MSSQLBCP:
    """This mixin provides utility functions for MSSQL's BCP. It serves as a mixin for BCPLoad and BCPDump subclasses
    """
    command = None
    connection = None
    delimiter = None
    batch_size = None

    def _run_command(self) -> subprocess.CompletedProcess:
        """This will run the instance's command via the BCP utility

        Returns: the result of the command line execution
        """
        return subprocess.run(f'bcp {self.command}', check=True)

    def _get_connection_string(self) -> str:
        """This method will generate a connection string using the associated Connection object. It supports Trusted
        connections (using Windows AD) and Credential connections (using SQL Server accounts).

        Returns: a BCP formatted connection string
        """
        auth = self.connection.auth
        if auth.type == 'Trusted':
            auth_string = f'-T'
        else:
            auth_string = f'-U {auth.username} -P {auth.password}'
        return f'-S {self.connection.host} {auth_string}'

    def _get_config_string(self) -> str:
        """This method will generate a configuration string. It supports the delimiter and batch size options.

        Returns: a BCP formatted configuration string
        """
        config = f'-c -t "{self.delimiter}"'
        if self.batch_size is not None:
            config = f'{config} -b {self.batch_size}'
        return config

    @staticmethod
    def _get_query_string(query) -> str:
        """This method will provide a BCP formatted query string using the query provided

        Args:
            query: the query whose results should be exported

        Returns: a BCP formatted query string
       """
        return f'"{query}"'

    @staticmethod
    def _get_output_file_string(output_file: pathlib.Path) -> str:
        """This method will provide a BCP formatted output file string using the file provided

        Args:
            output_file: the file to which data will be written

        Returns: a BCP formatted output file string
       """
        return f'queryout "{output_file.absolute()}"'

    @staticmethod
    def _get_input_file_string(input_file: pathlib.Path) -> str:
        """This method will provide a BCP formatted input file string using the file provided

        Args:
            input_file: the file from which data will be imported

        Returns: a BCP formatted input file string
        """
        return f'in "{input_file.absolute()}"'

    @staticmethod
    def _get_logging_string() -> str:
        """This method will generate a log file input string that will write the log file to the userprofile directory

        Returns: a BCP formatted log file string
        """
        log_file = LogFile()
        return f'-o "{log_file.file.absolute()}"'

    @staticmethod
    def _get_error_string() -> str:
        """This method will generate an error file input string that will write the error file to the userprofile directory

        Returns: a BCP formatted error file string
        """
        error_file = ErrorFile()
        return f'-e "{error_file.file.absolute()}"'
