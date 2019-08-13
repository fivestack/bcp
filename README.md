# BCP

< badges will go here >

**This is a python utility that allows users to import/export data to/from a database.**

---

# Overview

This library began as a wrapper around SQL Server's BCP utility. It makes some assumptions
about parameters to simplify the interface and allow the user to work natively in python.
Though it currently supports MSSQL, there are plans to extend support to other database dialects.

# Requirements

- Python 3.6+

This library purposely requires nothing outside of the standard library, beyond testing and documentation needs.
The intention is to maintain this status.

# Installation

This library is still in development. So you'll have to build it from
source in the meantime. I'll soon get around to publishing it on pypi, 
in which case you'll be able to install it using `pip`

    pip install bcp

# Examples

Import data:
```python
from bcp import BCP, Connection, DataFile

conn = Connection(host='HOST', driver='mssql', username='USER', password='PASSWORD')
my_bcp = BCP(conn)
file = DataFile(file_path='path/to/file.csv', delimiter=',')
my_bcp.load(file, 'table_name')
```

Export data:
```python
from bcp import BCP, Connection

conn = Connection(host='HOST', driver='mssql', username='USER', password='PASSWORD')
my_bcp = BCP(conn)
file = my_bcp.dump('select * from sys.tables')
print(file)  # %USERPROFILE%/bcp/data/<timestamp>.tsv
```

# Full Documentation

< readthedocs will go here >
