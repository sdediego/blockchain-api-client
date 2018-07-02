#!/usr/bin/env python
# encoding: utf-8

import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from logging.config import fileConfig
from os.path import dirname, join

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

@scheduler.scheduled_job()
def pools_job():
    pass

# Start queueing jobs
scheduler.start()
