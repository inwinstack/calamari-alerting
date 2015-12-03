# Copyright 2015 inWinStack Inc.
# All Rights Reserved.

"""
Exception definitions.
"""


class FunctionNotImplemented(Exception):
    """
    Function not yet finished
    """
    def __str__(self):
        return "This function is not yet available/completed."


class UnsupportedRequestType(Exception):
    """
    If a requested body type is not mapped
    """
    def __str__(self):
        return "Unknown request type."


class UnsupportedBodyType(Exception):
    """
    If a requested body type is not mapped
    """
    def __str__(self):
        return "This type of body is not supported for this API call."


class ClientException(Exception):
    """The base exception class for all exceptions this library raises."""


class ValidationError(ClientException):
    """Error in validation on API client side."""
    pass


class UnsupportedVersion(ClientException):
    """User is trying to use an unsupported version of the API."""
    pass


class CommandError(ClientException):
    """Error in CLI tool."""
    pass


class AuthorizationFailure(ClientException):
    """Cannot authorize API client."""
    pass


class ConnectionError(ClientException):
    """Cannot connect to API service."""
    pass


class ConnectionRefused(ConnectionError):
    """Connection refused while trying to connect to API service."""
    pass


class FormatException(Exception):
    """Cannot format data."""
    pass

