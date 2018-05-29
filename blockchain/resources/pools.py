#!/usr/bin/env python
# encoding: utf-8

import json
import re


class BlockchainAPIPool(object):
    """
    Get pools data behind Blockchain API.
    """

    def __init__(self, pools, *args, **kwargs):
        """
        Initialize Blockchain API for pools.

        :param json pools: json object with pools data.
        """
        self._pools = pools
        for key, value in self._pools.items():
            var_name = re.sub('[^0-9a-zA-Z]+', '', key).lower()
            setattr(self, '_{}'.format(var_name), {'pool': key, 'hashrate': value})

    def __str__(self):
        """
        Represent class via params string.

        :return str: class representarion.
        """
        return '<{} - Bitcoin pools>'.format(self.__class__.__name__)

    def get_info(self, pool):
        """
        Get pool hash rate distribution information.

        :param str pool: pool name.
        :return dict: pool hash rate contribution.
        """
        pool_name = list(filter(lambda name: name == pool, self._pools.keys()))
        if len(pool_name) > 0:
            var_name = re.sub('[^0-9a-zA-Z]+', '', pool_name[0]).lower()
            return vars(self)['_{}'.format(var_name)]

        return {}

    @property
    def pools(self):
        """
        Get mining pools list from Blockchain API.

        :return list: Bitcoin mining pools list.
        """
        return list(self._pools.keys())

    @property
    def response(self):
        """
        Get response from Blockchain API.

        :return str: Blockchain API response.
        """
        return json.dumps(self._pools)
