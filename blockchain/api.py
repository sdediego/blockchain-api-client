#!/usr/bin/env python
# encoding: utf-8

import configparser
import logging
import os
import requests

from slugify import slugify
from logging.config import fileConfig
from os.path import dirname, join
from dotenv import load_dotenv

from . import settings
from .exceptions import (BlockchainAPIClientError,
                         BlockchainAPIHttpRequestError)

# Custom logger
fileConfig(join(dirname(dirname(__file__)), 'logging.cfg'))
logger = logging.getLogger(__name__)

# Load .env file
dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)


class BlockchainAPIClient(object):
    """
    Enable Blockchain API use.
    """

    def __init__(self, data, api_url, api_key=None):
        """
        Initialize Blockchain API Client. If no API key provided there is a
        limit on the number of calls.

        :param str data: type of data to fetch (charts, stats, pools).
        :param str api_key: Key for unlimited calls to the API.
        """
        self._api_data = data
        self._api_url = api_url
        self._api_key = api_key
        self._request_params = {}

    def __str__(self):
        """
        Represent class via params string.

        :return str: class representarion.
        """
        params = {
            'classname': self.__class__.__name__,
            'data': self._api_data
        }
        for key, value in self._request_params.items():
            params.update({'{}'.format(key): value})
        return str(params)

    @classmethod
    def config(cls, data=None, filename='blockchain.cfg', section='api'):
        """
        Get BlockchainAPIClient class instance.

        :param str data: type of data to fetch (charts, stats, pools).
        :param str filename: Blockchain API Client configuration filename.
        :param str section: filename section to parse.
        :return cls: BlockchainAPIClient class instance.
        """
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
        """
        Set request parameters for api url.

        :param list args: list of arguments.
        :param dict kwargs: dict of keyword arguments.
        """
        for key, value in kwargs.items():
            if value is not None:
                self._request_params.update({key: value})

        if self._api_key is not None:
            self._request_params.update({'api_code': self._api_key})

    def call(self, *args, **kwargs):
        """
        Make request of data behind Blockchain API.

        1. Chart data:
        :param str chart: requested chart name.
        :param str timespan: duration of the chart.
        :param str rollingAverage: duration over which data should be averaged.
        :param datetime start: datetime at which to start the chart.
        :param str format: either json or csv.
        :param bool sampled: limits the number of datapoints returned if true.
        :return json: request result.

        2. Statistics data:
        :return json: request result.

        3. Pools data:
        :param str timespan: duration over which data is computed.
        :return json: request result.
        """
        if self._api_data == 'charts' and 'chart' in kwargs:
            self._api_url += '/{}'.format(kwargs.pop('chart'))

        self._set_request_params(*args, **kwargs)
        request = BlockchainAPIHttpRequest(self._api_url, self._request_params)
        request_url, json_response = request.fetch_json_response()
        request_result = BlockchainAPIHttpResponse(self._api_data, request_url, json_response)
        return request_result


class BlockchainAPIHttpRequest(object):
    """
    Enable Blockchain API data request.
    """

    def __init__(self, api_url=None, params=None):
        """
        Initialize request to Blockchain API.

        :param str api_url: blockchain api requested url.
        :param dict params: blockchain api url needed params.
        """
        self._api_url = api_url
        self._params = params

    def __str__(self):
        """
        Represent class via params string.

        :return str: class representarion.
        """
        request = {
            'classname': self.__class__.__name__,
            'url': self._api_url,
            'params': self._params,
        }
        return '<{classname}:\nurl: {url}\nparams: {params}>'.format(**request)

    def fetch_json_response(self):
        """
        Retrieve json object from API url.

        :return tuple: requested url and json response.
        """
        if self._api_url is not None and self._params is not None:
            http_response = self._http_request()
            request_url = http_response.url
            json_response = http_response.json()
            return request_url, json_response
        else:
            msg = 'Error: API URL and parameters must be provided.'
            raise BlockchainAPIHttpRequestError(msg)

    def fetch_csv_response(self):
        """
        Retrieve csv object from api url.
        """
        pass

    def _http_request(self):
        """
        Make http request to Blockchain API.

        :return obj: http object response.
        """
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
        """
        Get request url to Blockchain API.

        :return str: request url.
        """
        url = '{url}{query}'.format(url=self._api_url, query='?')
        for key, value in self._params.items():
            url += '{key}={value}&'.format(key=key, value=value)
        return url[:-1]


class BlockchainAPIHttpResponse(object):

    def __init__(self, data=None, url=None, response=None):
        self._data = data
        self._url = url
        self._response = response

        try:
            _temp = __import__('blockchain.resources', globals(), locals(), [self._data], 0)
        except ImportError as msg:
            logger.error('Error importing response class for %s data: %s', (data, msg))

        _resource = getattr(_temp, self._data, None)
        classname = getattr(_resource, settings.RESOURCES.get(self._data), None)
        if callable(classname):
            setattr(self, '{}'.format(self._data), classname.start(self._response, False))
        else:
            logger.error('Error initializing response class for %s data.', data)

    def __str__(self):
        request = {
            'classname': self.__class__.__name__,
            'data': self._data,
            'url': self._url,
        }
        return '<{classname}:\ndata: {data}\nurl: {url}>'.format(**request)

    def _generate_slug(self, response):
        name = response.get('name') or response.get('_name')
        response.update({'_slug': slugify(name)})
        return response

    @property
    def response(self):
        if self._data != 'charts':
            response = {
                '_name': self._data.capitalize(),
                '_values': self._response,
            }
        else:
            response = self._response
            response.pop('status', None)

        response = self._generate_slug(response)
        return response
