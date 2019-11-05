"""
This module contains data structures required to create and access files. Users will generally only need to use
DataFile directly. LogFile and ErrorFile are used indirectly by the BCP classes.

Example:

.. code-block:: python

    from bcp import DataFile

    # create a csv to write out my data
    my_file = DataFile(delimiter=',')
    print(my_file.path)  # %HOME%/bcp/data/<timestamp>.csv
"""
import abc
import datetime
from pathlib import Path

from .config import BCP_LOGGING_DIR, BCP_DATA_DIR


class File(abc.ABC):
    """
    This data structure creates a file handle given a file path.
    If the file path is not provided:

        - the current timestamp is used so that unique error, log, and data files can be created
        - the file will be created in the BCP_ROOT_DIR directory specified in config.py
    """
    _default_extension = None
    _default_directory = None
    _file = None

    @property
    def file(self) -> Path:
        return self._file

    @file.setter
    def file(self, value: Path = None):
        """
        This method generates a default file path object if none is provided

        Returns:
             a Path object that points to the file
        """
        if value is not None:
            self._file = value
        else:
            timestamp_format: str = '%Y_%m_%d_%H_%M_%S_%f'
            timestamp = datetime.datetime.now()
            file_name: str = '.'.join([timestamp.strftime(timestamp_format), self._default_extension])
            self._file = self._default_directory / Path(file_name)

    @property
    def path(self) -> Path:
        return self.file.absolute()


class DataFile(File):
    """
    This is a handle to a data file.

    Args:
        file_path: the path object to the file, if not provided, a default using the current timestamp will be created
        delimiter: the field delimiter for the data file
    """
    def __init__(self, file_path: Path = None, delimiter: str = None):
        self._default_directory = BCP_DATA_DIR
        self.delimiter = delimiter or '\t'
        if self.delimiter == '\t':
            self._default_extension = 'tsv'
        elif self.delimiter == ',':
            self._default_extension = 'csv'
        else:
            self._default_extension = 'dat'
        self.file = file_path


class LogFile(File):
    """
    This is a handle to a log file.

    Args:
        file_path: the path object to the file, if not provided, a default using the current timestamp will be created
    """
    def __init__(self, file_path: Path = None):
        self._default_directory = BCP_LOGGING_DIR
        self._default_extension = 'log'
        self.file = file_path


class ErrorFile(File):
    """
    This is a handle to an error file.

    Args:
        file_path: the path object to the file, if not provided, a default using the current timestamp will be created
    """
    def __init__(self, file_path: Path = None):
        self._default_directory = BCP_DATA_DIR
        self._default_extension = 'err'
        self.file = file_path
