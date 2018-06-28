#!/usr/bin/env python
# encoding: utf-8

# Settings for Blockchain API project


# Configure Blockchain API resources
RESOURCES = {
    'charts': 'BlockchainAPIChart',
    'stats': 'BlockchainAPIStatistics',
    'pools': 'BlockchainAPIPool',
}

# Blockchain Charts
CHARTS = [
    # Bitcoin stats
    'total-bitcoins',
    'market-price',
    'market-cap',
    'trade-volume',
    # Blockchain stats
    'blocks-size',
    'avg-block-size',
    'n-transactions-per-block',
    'median-confirmation-time',
    # Mining stats
    'hash-rate',
    'difficulty',
    'miners-revenue',
    'transaction-fees',
    'transaction-fees-usd',
    'cost-per-transaction-percent',
    'cost-per-transaction',
    # Network activity
    'n-unique-addresses',
    'n-transactions',
    'n-transactions-total',
    'transactions-per-second',
    'mempool-size',
    'utxo-count',
    'output-volume',
    'estimated-transaction-volume',
    'estimated-transaction-volume-usd',
]
