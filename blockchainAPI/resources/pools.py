#!/usr/bin/env python
# encoding: utf-8

import json


class BlockchainAPIPool(object):

    def __init__(self, pools, *args, **kwargs):
        self._pools = pools
        for key, value in self._pools.items():
            var_name = key.replace(" ", "").replace(".", "").lower()
            setattr(self, '_{}'.format(var_name), {'pool': key, 'hashrate': value})
