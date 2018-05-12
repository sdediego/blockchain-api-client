#!/usr/bin/env python
# encoding: utf-8

import json


class BlockchainAPIStatistics(object):

    def __init__(self, stats, keep=False):
        """
        Initialize Blockchain API for statistical data.

        :param json stats: json object with stats data.
        :param bool keep: flag to signal data keeping.
        """
        self.stats = stats if keep else None
        self.market_price_usd = stats.get('market_price_usd')
        self.hash_rate = stats.get('hash_rate')
        self.total_fees_btc = stats.get('total_fees_btc')
        self.n_btc_mined = stats.get('n_btc_mined')
        self.n_tx = stats.get('n_tx')
        self.n_blocks_mined = stats.get('n_blocks_mined')
        self.minutes_between_blocks = stats.get('minutes_between_blocks')
        self.total_bc = stats.get('totalbc')
        self.n_blocks_total = stats.get('n_blocks_total')
        self.estimated_transaction_volume_usd = stats.get('estimated_transaction_volume_usd')
        self.blocks_size = stats.get('blocks_size')
        self.miners_revenue_usd = stats.get('miners_revenue_usd')
        self.next_retarget = stats.get('nextretarget')
        self.difficulty = stats.get('difficulty')
        self.estimated_btc_sent = stats.get('estimated_btc_sent')
        self.miners_revenue_btc = stats.get('miners_revenue_btc')
        self.total_btc_sent = stats.get('total_btc_sent')
        self.trade_volume_btc = stats.get('trade_volume_btc')
        self.trade_volume_usd = stats.get('trade_volume_usd')
        self.timestamp = stats.get('timestamp')
