#!/usr/bin/env python
# encoding: utf-8


class BaseError(Exception):
    """
    Handle generic exception.
    """

    def __init__(self, msg, code=None):
        if code is not None:
            self.code = code
            msg += ': {exception}'.format(exception=self.code)
        self.msg = msg
        super(BaseError, self).__init__(self.msg)


class BlockchainAPIClientError(BaseError):
    """
    Handle exception for Blockchain API.
    """
    pass


class BlockchainAPIHttpRequestError(BaseError):
    """
    Handle exception for Blockchain API request error.
    """
    pass


class JSONFileWriterPipelineError(BaseError):
    """
    Handle exception for JSON file writer error.
    """
    pass


class MongoDBPipelineError(BaseError):
    """
    Handle exception for MongoDB pipeline error.
    """
    pass
