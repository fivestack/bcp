"""This module contains exceptions for this application."""


class DriverNotSupportedException(Exception):
    """This exception occurs when an unsupported driver is provided to a Connection or BCP object"""
    pass


class InvalidCredentialException(Exception):
    """This exception occurs when a username is provided without a password, or vice versa, for an Auth or BCP object"""
    pass
