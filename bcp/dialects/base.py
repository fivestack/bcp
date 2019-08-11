import abc

from ..files import DataFile
from ..connections import Connection


class BCPLoad(abc.ABC):
    """
    This is the abstract base class for all dialect-specific Dump implementations. It contains required methods and
    default values for all subclasses.

    Args:
        connection: the Connection object that points to the database from which we want to export data
        file: the file to be loaded into the database
        table: the table in which to land the data
    """

    def __init__(self, connection: Connection, file: DataFile, table: str):
        self.connection = connection
        self.file = file
        self.table = table

    @abc.abstractmethod
    def execute(self) -> str:
        """
        This will execute the the data import process.

        Returns:
             the name of the table that contains the data
        """
        raise NotImplementedError


class BCPDump(abc.ABC):
    """
    This is the abstract base class for all driver specific Dump implementations. It contains required methods and
    default values for all subclasses.

    Args:
        connection: the Connection object that points to the database from which we want to export data
        query: the query for the data to be exported
        file: the file to write the to, if not provided, a default will be created in the BCP_DATA_DIR
    """

    def __init__(self, connection: Connection, query: str, file: DataFile = None):
        self.connection = connection
        self.query = query
        self.file = file

    @abc.abstractmethod
    def execute(self) -> DataFile:
        """
        This will execute the data export process

        Returns:
             the data file object, which is useful when it is defaulted
        """
        raise NotImplementedError

    @property
    def file(self) -> DataFile:
        return self._file

    @file.setter
    def file(self, value: DataFile = None):
        """
        This setter will create a default file in the BCP_DATA_DIR if no file is provided.

        Args:
            value: the file to use instead of the default, if provided
        """
        if value is None:
            self._file = DataFile()
        else:
            self._file = value
