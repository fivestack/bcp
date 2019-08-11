from .exceptions import DriverNotSupportedException, InvalidCredentialException


class Auth:
    """This object collects the username and password for an authentication

    Args:
        username: username for the authorization
        password: password for the authorization
    """

    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password

    @property
    def type(self):
        """This property identifies the authorization type depending on the username/password provided. The two options
         for authorization are Trusted and Credential:
            * A Trusted connection is created when no username and no password are provided. In this case, the local
             user's credentials and authorization method are used.
            * A Credential connection is created when both a username and a password are provided.

        If only one of username and password are provided, this raises an InvalidCredentialException.
        """
        if self.username is None and self.password is None:
            return 'Trusted'
        elif self.username is not None and self.password is not None:
            return 'Credential'
        else:
            raise InvalidCredentialException

    def __repr__(self):
        return f'<Auth: {self.username}, Type: {self.type}>'


class Connection:
    """This object describes a connection to be used to instantiate a BCP instance. A host and driver must be supplied.
    A username/password combination can be supplied upon instantiation to automatically create an associated Auth
    object. Alternatively, this can be set as an attribute after instantiation. If the username/password are not
    provided, the connection will assume a Trusted authorization in the meantime.

    Args:
        host: the host where the database exists
        driver: the type of database (mssql, etc.)
        username: the username for authentication
        password: the password for authentication
    """

    def __init__(self, host: str, driver: str, username: str = None, password: str = None):
        self.host = host
        self.auth = Auth(username, password)
        self._set_driver(driver)

    def _set_driver(self, driver):
        """This method sets the type of connection and raises an exception for an unsupported driver.

        Args:
            driver: the type of database (mssql, etc.)
        """
        if driver in ['mssql']:
            self.driver = driver
        else:
            raise DriverNotSupportedException

    def __repr__(self):
        return f'<Connection: {self.host}+{self.auth.__repr__()}>'

    def __str__(self):
        """This will generate a BCP formatted connection string in the dialect of the associated database.

        Returns: a BCP formatted, dialect-specific, connection string
        """
        if self.driver == 'mssql':
            if self.auth.type == 'Trusted':
                auth_string = f'-T'
            else:
                auth_string = f'-U {self.auth.username} -P {self.auth.password}'
            return f'-S {self.host} {auth_string}'
