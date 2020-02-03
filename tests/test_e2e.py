"""
This collection of tests is intended to be run in a pre-prod environment that has access to all of the resources
required to fully execute BCP commands. These tests will be accessing the database, writing actual files, reading
actual files, and writing data to the database. These tests will require:

    - an instance of each supported database type (mssql, etc.)
    - an installation of the command line utility (if applicable) for each supported database (bcp, sqlcmd, etc.)
    - an account that has access to create/drop tables and insert data into those tables in said database

The settings that appear within each of the connection fixtures, and at the top of each test class, should be updated
to reflect the associated pre-prod environment.
"""
import pathlib
import subprocess

import pytest

from .conftest import STATIC_FILES, Connection, BCP, DataFile


@pytest.fixture
def mssql_bcp() -> 'BCP':
    """
    This will hand back a BCP wrapper around a connection to the development version of SQL Server installed locally.
    You can obtain a development copy of SQL Server for free here:

    https://www.microsoft.com/en-us/sql-server/sql-server-downloads

    The default settings will setup a database on localhost with the local user as admin, allowing you to run these
    tests.

    Returns:
        a BCP instance with a connection to the development version of SQL Server on localhost
    """
    conn = Connection(driver='mssql', host='localhost')
    return BCP(conn)


class TestMSSQL:

    database = 'master'
    schema = 'dbo'

    def test_mssql_can_dump_tables(self, mssql_bcp):
        query = f'''
            select s.name as schema_name, t.name as table_name
            from {self.database}.sys.tables t
            join {self.database}.sys.schemas s
            on s.schema_id = t.schema_id
        '''
        output_file_path = STATIC_FILES / pathlib.Path('output.dat')
        output_file = DataFile(file_path=output_file_path, delimiter='|~|')
        mssql_bcp.dump(query=query, output_file=output_file)
        assert output_file.file.is_file()
        output_file.file.unlink()

    def test_mssql_can_load_tables(self, mssql_bcp):
        table = f'{self.database}.{self.schema}.input_file'
        create = f'create table {table} (schema_name varchar(20), table_name varchar(100))'
        drop = f'drop table {table}'
        sqlcmd = f'sqlcmd -S {mssql_bcp.connection.host} -Q'
        subprocess.run(f'{sqlcmd} "{create}"', check=True)
        input_file_path = STATIC_FILES / pathlib.Path('input.dat')
        input_file = DataFile(file_path=input_file_path, delimiter='|~|')
        mssql_bcp.load(input_file=input_file, table=table)
        subprocess.run(f'{sqlcmd} "{drop}"', check=True)
        assert 1 == 1
