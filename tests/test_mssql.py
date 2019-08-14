import pathlib
import os
import pytest

from .context import exceptions, files, Connection, mssql


HOST = 'MSSQL,12345'
DRIVER = 'mssql'
USERNAME = 'user'
PASSWORD = 'pass'
BCP_ROOT_DIR = pathlib.Path(os.environ['USERPROFILE']) / pathlib.Path('bcp')


@pytest.fixture
def mssql_load_defaults():
    conn = Connection(host=HOST, driver=DRIVER)
    data_file = files.DataFile()
    return mssql.MSSQLLoad(conn, data_file, 'database.schema.table')


@pytest.fixture
def mssql_dump_defaults():
    conn = Connection(host=HOST, driver=DRIVER)
    data_file = files.DataFile()
    return mssql.MSSQLDump(conn, 'query', data_file)


class TestMSSQLConnectionCreation:

    def test_mssql_connection_creation_with_defaults(self):
        conn = Connection(host=HOST, driver=DRIVER)
        assert HOST == conn.host
        assert DRIVER == conn.driver
        assert 'Trusted' == conn.auth.type
        assert f'-S {HOST} -T' == str(conn)

    def test_mssql_connection_creation_with_credentials(self):
        conn = Connection(host=HOST, driver=DRIVER, username=USERNAME, password=PASSWORD)
        assert HOST == conn.host
        assert DRIVER == conn.driver
        assert 'Credential' == conn.auth.type
        assert f'-S {HOST} -U {USERNAME} -P {PASSWORD}' == str(conn)

    def test_mssql_connection_creation_with_username_and_no_password(self):
        with pytest.raises(exceptions.InvalidCredentialException):
            assert Connection(host=HOST, driver=DRIVER, username=USERNAME)

    def test_mssql_connection_creation_with_password_and_no_username(self):
        with pytest.raises(exceptions.InvalidCredentialException):
            assert Connection(host=HOST, driver=DRIVER, password=PASSWORD)


class TestMSSQLLoad:

    @pytest.mark.freeze_time
    def test_mssql_load_builds_expected_command_with_defaults(self, mssql_load_defaults):
        data_file = files.DataFile()
        log_file = files.LogFile()
        error_file = files.ErrorFile()
        table = 'database.schema.table'
        config = '-c -t "\t" -b 10000'
        expected = f'{table} in "{data_file.path}" -S {HOST} -T {config} -o "{log_file.path}" -e "{error_file.path}"'
        assert expected == mssql_load_defaults.command

    def test_mssql_load_builds_expected_config_with_defaults(self, mssql_load_defaults):
        expected = '-c -t "\t" -b 10000'
        assert expected == mssql_load_defaults.config

    def test_mssql_load_builds_expected_config_with_delimiter(self):
        conn = Connection(host=HOST, driver='mssql')
        data_file = files.DataFile(delimiter='|~|')
        mssql_load = mssql.MSSQLLoad(conn, data_file, 'table_name')
        expected = '-c -t "|~|" -b 10000'
        assert expected == mssql_load.config

    @pytest.mark.freeze_time('2019-05-01 01:00:00')
    def test_mssql_load_builds_expected_logging_string(self, mssql_load_defaults):
        log_file_path = BCP_ROOT_DIR / pathlib.Path('logs/2019_05_01_01_00_00_000000.log')
        expected = f'-o "{log_file_path.absolute()}"'
        assert expected == mssql_load_defaults.logging

    @pytest.mark.freeze_time('2019-07-01 01:00:00')
    def test_mssql_load_builds_expected_error_string(self, mssql_load_defaults):
        error_file_path = BCP_ROOT_DIR / pathlib.Path('data/2019_07_01_01_00_00_000000.err')
        expected = f'-e "{error_file_path.absolute()}"'
        assert expected == mssql_load_defaults.error


class TestMSSQLDump:

    @pytest.mark.freeze_time
    def test_mssql_dump_builds_expected_command_with_defaults(self, mssql_dump_defaults):
        data_file = files.DataFile()
        log_file = files.LogFile()
        query = 'query'
        config = '-c -t "\t"'
        expected = f'"{query}" queryout "{data_file.path}" -S {HOST} -T {config} -o "{log_file.path}"'
        assert expected == mssql_dump_defaults.command

    def test_mssql_dump_builds_expected_config_with_defaults(self, mssql_dump_defaults):
        expected = '-c -t "\t"'
        assert expected == mssql_dump_defaults.config

    def test_mssql_dump_builds_expected_config_with_delimiter(self):
        conn = Connection(host=HOST, driver='mssql')
        data_file = files.DataFile(delimiter='|~|')
        mssql_dump = mssql.MSSQLDump(conn, 'query', data_file)
        expected = '-c -t "|~|"'
        assert expected == mssql_dump.config

    @pytest.mark.freeze_time('2019-05-01 01:00:00')
    def test_mssql_dump_builds_expected_logging_string(self, mssql_dump_defaults):
        log_file_path = BCP_ROOT_DIR / pathlib.Path('logs/2019_05_01_01_00_00_000000.log')
        expected = f'-o "{log_file_path.absolute()}"'
        assert expected == mssql_dump_defaults.logging

