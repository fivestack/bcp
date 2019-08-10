import pathlib
import subprocess
import pytest
from .context import STATIC_FILES, BCP, Connection, files

HOST = 'MSSQL,12345'
USERNAME = 'user'
PASSWORD = 'pass'


@pytest.fixture
def mssql_bcp() -> BCP:
    connection = Connection(host=HOST, driver='mssql')
    return BCP(connection)


@pytest.fixture
def output_file() -> files.DataFile:
    file = files.DataFile(STATIC_FILES / pathlib.Path('output.dat'))
    return file


@pytest.fixture
def input_file() -> files.DataFile:
    file = files.DataFile(STATIC_FILES / pathlib.Path('input.dat'))
    return file


class TestMSSQL:

    database = 'SANDBOX'

    def test_mssql_can_dump_tables(self, mssql_bcp, output_file):
        query = f'''
            select s.name as schema_name, t.name as table_name
            from {self.database}.sys.tables t
            join {self.database}.sys.schemas s
            on s.schema_id = t.schema_id
        '''
        mssql_bcp.dump(query, output_file)
        file_exists = output_file.file.is_file()
        if file_exists:
            output_file.file.unlink()
        assert True is file_exists

    def test_mssql_can_load_tables(self, mssql_bcp, input_file):
        command = f'sqlcmd -S {HOST} -Q "create table {self.database}.data.input_file (schema_name varchar(20), table_name varchar(100))"'
        subprocess.run(command, check=True)
        table = f'{self.database}.data.input_file'
        mssql_bcp.load(input_file, table)
        command = f'sqlcmd -S {HOST} -Q "drop table {self.database}.data.input_file"'
        subprocess.run(command, check=True)
        assert 1 == 1
