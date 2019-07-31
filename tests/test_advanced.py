import pathlib
import subprocess
import pytest
from .context import bcp, STATIC_FILES

HOST = 'MSSQL,12345'


@pytest.fixture
def mssql_bcp() -> bcp.BCP:
    connection = bcp.Connection(host=HOST, driver='mssql')
    return bcp.BCP(connection)


@pytest.fixture
def output_file() -> pathlib.Path:
    return STATIC_FILES / pathlib.Path('output.dat')


@pytest.fixture
def input_file() -> pathlib.Path:
    return STATIC_FILES / pathlib.Path('input.dat')


class TestMSSQL:

    database = 'SANDBOX'

    def test_mssql_connection(self, mssql_bcp):
        expected = f'-S {HOST} -T'
        actual_dump = mssql_bcp.bcp_dump._get_connection_string()
        actual_load = mssql_bcp.bcp_load._get_connection_string()
        assert expected == actual_dump
        assert expected == actual_load

    def test_mssql_can_dump_tables(self, mssql_bcp, output_file):
        query = f'select s.name as schema_name, t.name as table_name from {self.database}.sys.tables t join {self.database}.sys.schemas s on s.schema_id = t.schema_id'
        mssql_bcp.dump(query, output_file)
        file_exists = output_file.is_file()
        if file_exists:
            output_file.unlink()
        assert True is file_exists

    def test_mssql_can_load_tables(self, mssql_bcp, input_file):
        command = f'sqlcmd -S {HOST} -Q "create table {self.database}.data.input_file (schema_name varchar(20), table_name varchar(100))"'
        subprocess.run(command, check=True)
        table = f'{self.database}.data.input_file'
        mssql_bcp.load(input_file, table)
        command = f'sqlcmd -S {HOST} -Q "drop table {self.database}.data.input_file"'
        subprocess.run(command, check=True)
        assert 1 == 1
