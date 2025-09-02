"""
Intacct REST SDK Exceptions
"""


class IntacctRESTSDKError(Exception):
    """The base exception class for Intacct REST SDK.

    Parameters:
        msg (str): Short description of the error.
        response: Error response from the API call.
    """

    def __init__(self, msg, response=None):
        super(IntacctRESTSDKError, self).__init__(msg)
        self.message = msg
        self.response = response

    def __str__(self):
        return repr(self.message)


class InvalidTokenError(IntacctRESTSDKError):
    """Wrong/expired/non-existing access token"""


class BadRequestError(IntacctRESTSDKError):
    """Some of the parameters (HTTP params or request body) are wrong, 4xx error"""


class InternalServerError(IntacctRESTSDKError):
    """Anything 5xx"""
