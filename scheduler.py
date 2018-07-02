#!/usr/bin/env python
# encoding: utf-8

import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from logging.config import fileConfig
from os.path import dirname, join

from blockchain.api import BlockchainAPIClient
from blockchain.pipelines import MongoDBPipeline

# Custom logger
fileConfig(join(dirname(dirname(__file__)), 'logging.cfg'))
logger = logging.getLogger(__name__)

scheduler = BlockingScheduler()


@scheduler.scheduled_job()
def charts_job():
    pass

@scheduler.scheduled_job()
def stats_job():
    pass

@scheduler.scheduled_job(id='pools', trigger='cron', day_of_week='mon-sun', hour=0)
def pools_job():
    logger.info('Fetching bitcoin mining pools data.')

    api = BlockchainAPIClient('pools')
    result = api.call(timespan='5days')

    logger.info('Persisting fetched data in MongoDB: %s', result)
    mongo = MongoDBPipeline.config()
    mongo.open_connection()
    mongo.persist_data(result.response)
    mongo.close_connection()
    logger.info('Data successfully persisted.')

# Start queueing jobs
scheduler.start()
