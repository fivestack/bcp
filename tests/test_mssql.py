import pathlib
import os
import pytest

import bcp.dialects.mssql
from .context import exceptions, Connection, mssql


HOST = 'MSSQL,12345'
USERNAME = 'user'
PASSWORD = 'pass'


@pytest.fixture
def mssql_connection():
    return bcp.Connection(host='SERVER,12345', driver='mssql')


@pytest.fixture
def mssql_load(mssql_connection):
    return mssql.MSSQLLoad(mssql_connection)


@pytest.fixture
def mssql_dump(mssql_connection):
    return mssql.MSSQLDump(mssql_connection)


@pytest.fixture
def error_file_path():
    user_profile = pathlib.Path(os.environ['USERPROFILE'])
    return user_profile / pathlib.Path('bcp/logs/2019_05_01_01_00_00_000000.err')


@pytest.fixture
def log_file_path():
    user_profile = pathlib.Path(os.environ['USERPROFILE'])
    return user_profile / pathlib.Path('bcp/logs/2019_05_01_01_00_00_000000.log')


class TestMSSQLConnectionCreation:

    def test_mssql_connection_with_no_credentials(self, mssql_bcp):
        expected = f'-S {HOST} -T'
        connection = Connection(host=HOST, driver='mssql')
        assert expected == str(connection)

    def test_mssql_connection_with_credentials(self, mssql_bcp):
        expected = f'-S {HOST} -U {USERNAME} -P {PASSWORD}'
        connection = Connection(host=HOST, driver='mssql', username=USERNAME, password=PASSWORD)
        assert expected == str(connection)

    def test_mssql_connection_with_username_and_no_password(self):
        with pytest.raises(exceptions.InvalidCredentialException):
            assert Connection(host=HOST, driver='mssql', username=USERNAME)

    def test_mssql_connection_with_password_and_no_username(self):
        with pytest.raises(exceptions.InvalidCredentialException):
            assert Connection(host=HOST, driver='mssql', password=PASSWORD)


@pytest.mark.freeze_time('2019-05-01 01:00:00')
class TestMSSQLLoad:

    def test_mssql_bcp_load_builds_expected_command(self, mssql_load, log_file_path, error_file_path):
        data_file_path = pathlib.Path(__file__) / pathlib.Path('sample_data/mssql_bcp_load.dat')
        table = 'database.schema.table'
        mssql_load._build_command(data_file_path, table)
        expected = f'database.schema.table in "{data_file_path.absolute()}" -S SERVER,12345 -T -c -t "\t" -b 10000 -o "{log_file_path.absolute()}" -e "{error_file_path.absolute()}"'
        actual = mssql_load.command
        assert expected == actual

    def test_mssql_load_builds_expected_config_with_delimiter_and_batch_size(self, mssql_load):
        mssql_load.delimiter = '|~|'
        mssql_load.batch_size = 1776
        expected = '-c -t "|~|" -b 1776'
        actual = mssql_load._get_config_string()
        assert expected == actual

    def test_mssql_load_builds_expected_config_with_batch_size(self, mssql_load):
        mssql_load.batch_size = 1776
        expected = '-c -t "\t" -b 1776'
        actual = mssql_load._get_config_string()
        assert expected == actual

    def test_mssql_load_builds_expected_config_with_delimiter(self, mssql_load):
        mssql_load.delimiter = '|~|'
        expected = '-c -t "|~|" -b 10000'
        actual = mssql_load._get_config_string()
        assert expected == actual

    def test_mssql_load_builds_expected_config_with_defaults(self, mssql_load):
        assert mssql_load._get_config_string() == '-c -t "\t" -b 10000'

    def test_mssql_load_builds_expected_logging_string(self, mssql_load, log_file_path):
        expected = f'-o "{log_file_path.absolute()}"'
        actual = mssql_load._get_logging_string()
        assert expected == actual

    def test_mssql_load_builds_expected_error_string(self, mssql_load, error_file_path):
        expected = f'-e "{error_file_path.absolute()}"'
        actual = mssql_load._get_error_string()
        assert expected == actual


@pytest.mark.freeze_time('2019-05-01 01:00:00')
class TestMSSQLDump:

    def test_mssql_bcp_dump_builds_expected_command(self, mssql_dump, log_file_path):
        data_file_path = pathlib.Path(__file__) / pathlib.Path('data/file/path.dat')
        query = 'select t2.column, t.* from schema.table t join schema2.table2 t2 on t2.fk = t.pk'
        mssql_dump._build_command(query, data_file_path)
        expected = f'"select t2.column, t.* from schema.table t join schema2.table2 t2 on t2.fk = t.pk" queryout "{data_file_path.absolute()}" -S SERVER,12345 -T -c -t "\t" -o "{log_file_path.absolute()}"'
        actual = mssql_dump.command
        assert expected == actual

    def test_mssql_dump_builds_expected_config_with_delimiter_and_batch_size(self, mssql_dump):
        mssql_dump.delimiter = '|~|'
        mssql_dump.batch_size = 1776
        expected = '-c -t "|~|" -b 1776'
        actual = mssql_dump._get_config_string()
        assert expected == actual

    def test_mssql_dump_builds_expected_config_with_batch_size(self, mssql_dump):
        mssql_dump.batch_size = 1776
        expected = '-c -t "\t" -b 1776'
        actual = mssql_dump._get_config_string()
        assert expected == actual

    def test_mssql_dump_builds_expected_config_with_delimiter(self, mssql_dump):
        mssql_dump.delimiter = '|~|'
        expected = '-c -t "|~|"'
        actual = mssql_dump._get_config_string()
        assert expected == actual

    def test_mssql_dump_builds_expected_config_with_defaults(self, mssql_dump):
        assert mssql_dump._get_config_string() == '-c -t "\t"'

    def test_mssql_dump_builds_expected_logging_string(self, mssql_dump, log_file_path):
        expected = f'-o "{log_file_path.absolute()}"'
        actual = mssql_dump._get_logging_string()
        assert expected == actual

    def test_mssql_dump_builds_expected_error_string(self, mssql_dump, error_file_path):
        expected = f'-e "{error_file_path.absolute()}"'
        actual = mssql_dump._get_error_string()
        assert expected == actual
