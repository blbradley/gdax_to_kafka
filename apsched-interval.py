import logging

from apscheduler.schedulers.background import BlockingScheduler
import requests


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

sched = BlockingScheduler()

def my_job():
    logging.warning('foo')

sched.add_job(my_job, 'interval', seconds=1)
sched.start()
