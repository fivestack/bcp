import pathlib
import os


def get_directory(name: str) -> pathlib.Path:
    """This function creates a bcp directory (or returns the existing directory) in the user's directory
     to store logs and other artifacts

    Args:
        name: name of the directory within %USERPROFILE%/bcp/ to be created / returned

    Returns: the directory as a Path object
    """
    user_profile = pathlib.Path(os.environ['USERPROFILE'])
    bcp_root = user_profile / pathlib.Path('bcp')
    directory = bcp_root / pathlib.Path(name)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


BCP_LOGGING_DIRECTORY: pathlib.Path = get_directory('logs')
