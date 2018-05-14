#!/usr/bin/env python
# encoding: utf-8

import json


class BlockchainAPIPool(object):

    def __init__(self, pools, *args, **kwargs):
        self._pools = pools
        for key, value in self._pools.items():
            var_name = key.replace(" ", "").replace(".", "").lower()
            setattr(self, '_{}'.format(var_name), {'pool': key, 'hashrate': value})

    def __str__(self):
        return '<{} - Bitcoin pools>'.format(self.__class__.__name__)

    def get_info(self, pool):
        pool_name = list(filter(lambda name: name == pool, self._pools.keys()))
        if len(pool_name) > 0:
            var_name = pool_name[0].replace(" ", "").replace(".", "").lower()
            return vars(self)['_{}'.format(var_name)]

        return {}

    @property
    def pools(self):
        return list(self._pools.keys())

    @property
    def response(self):
        return json.dumps(self._pools)
