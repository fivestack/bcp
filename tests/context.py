from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).parent
PROJECT_ROOT = PACKAGE_ROOT.parent
STATIC_FILES = PACKAGE_ROOT / Path('static_files')

sys.path.insert(0, str(PROJECT_ROOT.absolute()))

from bcp import connections, core, files, exceptions, Connection, BCP, DataFile
from bcp.dialects import mssql
