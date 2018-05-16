#!/usr/bin/env python
# encoding: utf-8


class BlockchainAPIClient(object):

    def __init__(self, data, api_url, api_key=None):
        self._api_data = data
        self._api_url = api_url
        self._api_key = api_key
        self._request_params = {}

    def __str__(self):
        params = {
            'classname': self.__class__.__name__,
            'data': self._api_data
        }
        for key, value in self._request_params.items():
            params.update({'{}'.format(key): value})
        return str(params)
