#!/usr/bin/env python
# encoding: utf-8

import json


class BlockchainAPIChart(object):
    """
    Get chart data behind Blockchain API.
    """
    def __init__(self, chart, keep=False):
        """
        Initialize Blockchain API for chart.

        :param json chart: json object with chart data.
        :param bool keep: flag to signal data keeping.
        """
        self.chart = chart if keep else None
        self.status = chart.get('status')
        self.name = chart.get('name')
        self.unit = chart.get('unit')
        self.period = chart.get('period')
        self.description = chart.get('description')
        self.values = chart.get('values')

    def __str__(self):
        """
        Represent class via params string.

        :return str: class representarion.
        """
        chart = {
            'classname': self.__class__.__name__,
            'name': self.name,
            'description': self.description,
        }
        return '<{classname} - {chart}: {description}>'.format(**chart)

    @property
    def response(self):
        """
        Get response from Blockchain API.

        :return str: Blockchain API response.
        """
        response = {}
        if self.chart is not None:
            response = self.chart

        return json.dumps(response)
