"""Python wrapper around the bcp utility for MSSQL"""
__version__ = '0.2.1'
name = 'bcp'

from .core import BCP
from .connections import Connection
from .files import DataFile
