#!/usr/bin/env python
# encoding: utf-8

import configparser
import os

from .exceptions import BlockchainAPIClientError, BlockchainAPIHttpRequestError


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

    def _set_request_params(self, *args, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                self._request_params.update({key: value})

        if self._api_key is not None:
            self._request_params.update({'api_code': self._api_key})

    def call(self, *args, **kwargs):
        if self._api_data == 'charts' and 'chart' in kwargs:
            self._api_url += '/{}'.format(kwargs.pop('chart'))

        self._set_request_params(*args, **kwargs)
        request = BlockchainAPIHttpRequest(self._api_url, self._request_params)
        request_url, json_response = request.fetch_json_response()
        request_result = BlockchainAPIHttpResponse(self._api_data, request_url, json_response)
        return request_result


class BlockchainAPIHttpRequest(object):

    def __init__(self, api_url=None, params=None):
        self._api_url = api_url
        self._params = params

    def __str__(self):
        request = {
            'classname': self.__class__.__name__,
            'url': self._api_url,
            'params': self._params,
        }
        return '<{classname}:\nurl: {url}\nparams: {params}>'.format(**request)

    def fetch_json_response(self):
        if self._api_url is not None and self._params is not None:
            http_response = self._https_request()
            request_url = http_response.url
            json_response = http_response.json()
            return request_url, json_response
        else:
            msg = 'Error: API URL and parameters must be provided.'
            raise BlockchainAPIHttpRequestError(msg)

    def fetch_csv_response(self):
        pass

    def _https_request(self):
        encoded_params = {}
        for key, value in self._params.items():
            value = str(value).encode(encoding='utf-8')
            encoded_params.update({key: value})

        http_response = requests.get(self._api_url, params=encoded_params)
        if http_response.status_code == requests.codes.ok:
            return http_response
        else:
            msg = 'Error: url {}, params {}'.format(self._api_url, self._params)
            code = http_response.status_code
            raise BlockchainAPIHttpRequestError(msg, code)

    @property
    def request_url(self):
        url = '{url}{query}'.format(url=self._api_url, query='?')
        for key, value in self._params.items():
            url += '{key}={value}&'.format(key=key, value=value)
        return url[:-1]


class BlockchainAPIHttpResponse(object):
    pass
