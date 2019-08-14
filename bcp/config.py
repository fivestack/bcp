"""
This module creates directories (or returns existing directories) to store logs, data and other artifacts.

.. note::
    This application defaults to creating a 'bcp' directory inside of the %userprofile% directory. However, this can be
    overridden by setting a value for the environmental variable BCP_ROOT_DIR. The structure within this root directory
    will always be the same.
"""
from pathlib import Path
import os


def get_bcp_root_dir() -> Path:
    user_profile = Path(os.environ['USERPROFILE'])
    bcp_root_dir_default = user_profile / Path('bcp')
    bcp_root_dir = Path(os.environ.get('BCP_ROOT_DIR', bcp_root_dir_default.absolute()))
    return bcp_root_dir


BCP_ROOT_DIR = get_bcp_root_dir()
BCP_DATA_DIR = BCP_ROOT_DIR / Path('data')
BCP_LOGGING_DIR = BCP_ROOT_DIR / Path('logs')

BCP_ROOT_DIR.mkdir(parents=True, exist_ok=True)
BCP_DATA_DIR.mkdir(parents=True, exist_ok=True)
BCP_LOGGING_DIR.mkdir(parents=True, exist_ok=True)
