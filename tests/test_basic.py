import pathlib
import os

import pytest

from .context import files, exceptions, Connection, BCP, STATIC_FILES

HOST = 'SERVER,12345'


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
        expected_data_file_path = self.user_profile / pathlib.Path('bcp/data/2018_07_01_01_00_00_000000.dat')
        assert expected_data_file_path.absolute() == data_file.path
        assert '\t' == data_file.delimiter

    @pytest.mark.freeze_time('2018-05-01 01:00:00')
    def test_data_file_creation_with_parameters(self):
        file_path = STATIC_FILES / pathlib.Path('input.dat')
        data_file = files.DataFile(file_path=file_path, delimiter='|~|')
        expected_data_file_path = file_path
        assert expected_data_file_path.absolute() == data_file.path
        assert '|~|' == data_file.delimiter


def test_connection_creation_with_unsupported_driver_raises_exception():
    with pytest.raises(exceptions.DriverNotSupportedException):
        assert Connection(host=HOST, driver='unsupported')


def test_bcp_creation_with_unsupported_connection_raises_exception():
    connection = Connection(host=HOST, driver='mssql')
    connection.driver = 'unsupported'
    with pytest.raises(exceptions.DriverNotSupportedException):
        assert BCP(connection)
