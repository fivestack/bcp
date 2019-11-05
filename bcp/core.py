"""
This is the core module of the library, containing the primary interface over the functionality of bcp. Along with its
dependencies on Connection and DataFile, it serves as the entry point to the library. Simply create a Connection, pass
it in to the BCP object, and then use load() or dump() to read data into and out of a database. See the methods below
for examples.
"""

from .exceptions import DriverNotSupportedException
from .connections import Connection
from .files import DataFile
from .dialects import mssql


class BCP:
    """
    This is the interface over dialect-specific classes that provides generic methods to load/dump data to/from a
    database.

    Args:
        connection: a Connection object that contains authorization details and database details

    Example:

    .. code-block:: python

        from bcp import BCP, Connection, DataFile

        conn = Connection('host', 'mssql', 'username', 'password')
        my_bcp = BCP(conn)
    """

    def __init__(self, connection: Connection):
        self.connection = connection

    def load(self, input_file: DataFile, table: str) -> str:
        """
        This method provides an interface to the lower level dialect-specific BCP load classes.

        Args:
            input_file: the file to be loaded into the database
            table: the table in which to land the data

        Returns:
             the name of the table that contains the data

        Example:

        .. code-block:: python

            from bcp import BCP, Connection, DataFile

            conn = Connection(host='HOST', driver='mssql', username='USER', password='PASSWORD')
            my_bcp = BCP(conn)
            file = DataFile(file_path='path/to/file.csv', delimiter=',')
            my_bcp.load(file, 'table_name')
        """
        if self.connection.driver == 'mssql':
            load = mssql.MSSQLLoad(self.connection, input_file, table)
        else:
            raise DriverNotSupportedException
        return load.execute()

    def dump(self, query: str, output_file: DataFile = None) -> DataFile:
        """
        This method provides an interface to the lower level dialect-specific BCP dump classes.

        Args:
            query: the query whose results should be saved off to a file
            output_file: the file to which the data should be saved, if no file is provided, one will be created in
                the BCP_DATA_DIR

        Returns:
             the data file object, which is useful when it is defaulted

        Example:

        .. code-block:: python

            from bcp import BCP, Connection

            conn = Connection(host='HOST', driver='mssql', username='USER', password='PASSWORD')
            my_bcp = BCP(conn)
            file = my_bcp.dump('select * from sys.tables')
            print(file)  # %USERPROFILE%/bcp/data/<timestamp>.tsv
        """
        if self.connection.driver == 'mssql':
            dump = mssql.MSSQLDump(self.connection, query, output_file)
        else:
            raise DriverNotSupportedException
        return dump.execute()

    def __repr__(self):
        return f'BCP(connection={repr(self.connection)})'
