import datetime
import pathlib
import os
import pytest
from .context import files, exceptions, bcp


@pytest.fixture
def unsupported_connection():
    connection = bcp.Connection(host='SERVER,12345', driver='mssql')
    connection.driver = 'unsupported'
    return connection


class TestFileCreation:

    user_profile = pathlib.Path(os.environ['USERPROFILE'])

    @pytest.mark.freeze_time('2019-05-01 01:00:00')
    def test_log_file_is_created(self):
        log_file = files.LogFile(datetime.datetime.now())
        log_file_path = self.user_profile / pathlib.Path('bcp/logs/2019_05_01_01_00_00_000000.log')
        expected = log_file_path.absolute()
        actual = log_file.file.absolute()
        assert expected == actual

    @pytest.mark.freeze_time('2019-07-01 01:00:00')
    def test_error_file_is_created(self):
        error_file = files.ErrorFile(datetime.datetime.now())
        error_file_path = self.user_profile / pathlib.Path('bcp/logs/2019_07_01_01_00_00_000000.err')
        expected = error_file_path.absolute()
        actual = error_file.file.absolute()
        assert expected == actual


def test_unsupported_connection_raises_exception():
    with pytest.raises(exceptions.DriverNotSupportedException):
        assert bcp.Connection(host='SERVER,12345', driver='unsupported')


def test_bcp_unsupported_connection_raises_exception(unsupported_connection):
    with pytest.raises(exceptions.DriverNotSupportedException):
        assert bcp.BCP(unsupported_connection)
