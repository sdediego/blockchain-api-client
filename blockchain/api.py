#!/usr/bin/env python
# encoding: utf-8

import configparser
import os

from .exceptions import BlockchainAPIClientError


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

    @classmethod
    def config(cls, data=None, filename='blockchain.cfg', section='api'):
        parser = configparser.ConfigParser()
        parser.read(filename)
        if parser.has_section(section):
            base_url = parser.get(section, 'base_url')
            data_url = parser.get(section, data)
            api_key = os.getenv('API_KEY')
            return cls(data, base_url + data_url, api_key)
        else:
            msg = 'Section {} not found in {} file'.format(section, filename)
            raise BlockchainAPIClientError(msg)

    def call(self, *args, **kwargs):
        if self._api_data == 'charts' and 'chart' in kwargs:
            self._api_url += '/{}'.format(kwargs.pop('chart'))

        self._set_request_params(*args, **kwargs)
        request = BlockchainAPIHttpRequest(self._api_url, self._request_params)
        request_url, json_response = request.fetch_json_response()
        request_result = BlockchainAPIHttpResponse(self._api_data, request_url, json_response)
        return request_result
