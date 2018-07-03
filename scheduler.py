#!/usr/bin/env python
# encoding: utf-8

import logging
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from logging.config import fileConfig
from os.path import dirname, join

from blockchain.api import BlockchainAPIClient
from blockchain.pipelines import MongoDBPipeline

# Custom logger
fileConfig(join(dirname(dirname(__file__)), 'logging.cfg'))
logger = logging.getLogger(__name__)

scheduler = BlockingScheduler()


def fetch_and_persist_data(data, *args, **kwargs):
    # Retrieve blockchain data
    api = BlockchainAPIClient(data)
    result = api.call(**kwargs)
    # Persist retrieved data
    logger.info('Persisting fetched data in MongoDB: %s', result)
    mongo = MongoDBPipeline.config()
    mongo.open_connection()
    mongo.persist_data(result.response)
    mongo.close_connection()
    logger.info('Data successfully persisted.')
    time.sleep(2)

@scheduler.scheduled_job()
def charts_job():
    pass

@scheduler.scheduled_job(id='stats', trigger='cron', day_of_week='mon-sun', hour=0)
def stats_job():
    logger.info('Fetching blockchain statistical data.')
    fetch_and_persist_data('stats')

@scheduler.scheduled_job(id='pools', trigger='cron', day_of_week='mon-sun', hour=0)
def pools_job():
    logger.info('Fetching bitcoin mining pools data.')
    fetch_and_persist_data('pools', timespan='5days')

# Start queueing jobs
scheduler.start()
