"""Python wrapper around the bcp utility for MSSQL"""
__version__ = '0.2.1'
name = 'bcp'

from .connection import Connection
from .core import BCP
