import pathlib
import os

import pytest

from .conftest import files, exceptions, connections, BCP, Connection, STATIC_FILES

DRIVER = 'mssql'
HOST = 'SERVER'
PORT = 12345
USERNAME = 'user'
PASSWORD = '1234'


class TestFiles:

    user_profile = pathlib.Path(os.environ['USERPROFILE'])

    @pytest.mark.freeze_time('2019-05-01 01:00:00')
    def test_log_file_creation_with_defaults(self):
        log_file = files.LogFile()
        expected_log_file_path = self.user_profile / pathlib.Path('bcp/logs/2019_05_01_01_00_00_000000.log')
        assert expected_log_file_path.absolute() == log_file.path

    @pytest.mark.freeze_time('2019-07-01 01:00:00')
    def test_error_file_creation_with_defaults(self):
        error_file = files.ErrorFile()
        expected_error_file_path = self.user_profile / pathlib.Path('bcp/data/2019_07_01_01_00_00_000000.err')
        assert expected_error_file_path.absolute() == error_file.path

    @pytest.mark.freeze_time('2018-07-01 01:00:00')
    def test_data_file_creation_with_defaults(self):
        data_file = files.DataFile()
        expected_data_file_path = self.user_profile / pathlib.Path('bcp/data/2018_07_01_01_00_00_000000.tsv')
        assert expected_data_file_path.absolute() == data_file.path
        assert '\t' == data_file.delimiter

    @pytest.mark.freeze_time('2018-05-01 01:00:00')
    def test_data_file_creation_with_path_and_delimiter(self):
        file_path = STATIC_FILES / pathlib.Path('input.dat')
        data_file = files.DataFile(file_path=file_path, delimiter='|~|')
        expected_data_file_path = file_path
        assert expected_data_file_path.absolute() == data_file.path
        assert '|~|' == data_file.delimiter

    @pytest.mark.freeze_time('2017-05-01 01:00:00')
    def test_data_file_creation_with_no_path_and_comma_delimiter(self):
        data_file = files.DataFile(delimiter=',')
        expected_data_file_path = self.user_profile / pathlib.Path('bcp/data/2017_05_01_01_00_00_000000.csv')
        assert expected_data_file_path.absolute() == data_file.path
        assert ',' == data_file.delimiter

    @pytest.mark.freeze_time('2017-08-01 01:00:00')
    def test_data_file_creation_with_no_path_and_tab_delimiter(self):
        data_file = files.DataFile(delimiter='\t')
        expected_data_file_path = self.user_profile / pathlib.Path('bcp/data/2017_08_01_01_00_00_000000.tsv')
        assert expected_data_file_path.absolute() == data_file.path
        assert '\t' == data_file.delimiter


def test_connection_creation_with_unsupported_driver_raises_exception():
    with pytest.raises(exceptions.DriverNotSupportedException):
        assert Connection(host=HOST, driver='unsupported')


def test_auth_has_correct_repr():
    auth = connections.Auth(username='user', password='pass')
    assert f'Auth(username={USERNAME}, password={len(PASSWORD)})' == repr(auth)


def test_connection_has_correct_repr():
    conn = Connection(driver='mssql', host=HOST, port=PORT, username=USERNAME, password=PASSWORD)
    assert f'Connection(driver={DRIVER}, host={HOST}, port={PORT}, auth=Auth(username={USERNAME},' \
           f' password={len(PASSWORD)}))' == repr(conn)


def test_bcp_has_correct_repr():
    conn = Connection(driver='mssql', host=HOST, port=PORT, username=USERNAME, password=PASSWORD)
    my_bcp = BCP(conn)
    assert f'BCP(connection=Connection(driver={DRIVER}, host={HOST}, port={PORT}, auth=Auth(username={USERNAME},' \
           f' password={len(PASSWORD)})))' == repr(my_bcp)
