"""This is a python utility that allows users to import/export data to/from a database."""
__version__ = '0.2.1'
name = 'bcp'

from .core import BCP
from .connections import Connection
from .files import DataFile
