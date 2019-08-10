import abc
import datetime
import pathlib
from .config import BCP_LOGGING_DIRECTORY


class File(abc.ABC):
    """This object creates a file handle given a timestamp so that unique error and log files can be created.
    The file will be created in the BCP log directory specified in config.py.

    Args:
        timestamp: the timestamp to be used to generate the file, defaulted to when the file instance is created
    """

    def __init__(self, timestamp: datetime = None):
        self.directory = BCP_LOGGING_DIRECTORY
        if timestamp is not None:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.datetime.now()
        self.extension = None

    @property
    def file(self) -> pathlib.Path:
        """This method returns a file path object with consistent naming format

        Returns: a Path object that points to the new (yet to be created) file
        """
        timestamp_format: str = '%Y_%m_%d_%H_%M_%S_%f'
        file_name: str = '.'.join([self.timestamp.strftime(timestamp_format), self.extension])
        file_path: pathlib.Path = self.directory / pathlib.Path(file_name)
        return file_path

    @property
    def path(self) -> pathlib.Path:
        return self.file.absolute()


class LogFile(File):
    """This is a handle to the log file to be generated"""

    def __init__(self, timestamp: datetime = None):
        super().__init__(timestamp)
        self.extension = 'log'


class ErrorFile(File):
    """This is a handle to the error file to be generated"""

    def __init__(self, timestamp: datetime = None):
        super().__init__(timestamp)
        self.extension = 'err'


class DataFile(File):
    """This is a handle to the data file to be generated"""

    def __init__(self, timestamp: datetime = None, delimiter: str = ','):
        super().__init__(timestamp)
        self.extension = 'dat'
        self.delimiter = delimiter
