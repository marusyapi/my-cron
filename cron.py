import logging
import os
import subprocess
import sys
import time
from datetime import datetime

from crontab import CronTab

import constants

crontab = None
cron_tasks = []


def get_cron(file_path):
    global crontab
    try:
        crontab = CronTab(tabfile=file_path, user='marusya')
    except Exception:
        raise FileNotFoundError("Wrong path")


def get_cron_tasks():
    cron_tasks.clear()
    for cron in crontab:
        cron_tasks.append(cron)


def run_cron():
    cron_time = None
    cron_command = None

    for cron in crontab:
        cron_time = cron.schedule(date_from=datetime.now()).get_next().strftime(constants.DEFAULT_CRON_DATE_FORMAT)
        print(cron_time)
        cron_command = cron.command
        print(cron_command)

    while True:
        try:
            if cron_time == datetime.now().strftime(constants.DEFAULT_CRON_DATE_FORMAT):
                pid = os.fork()
                if pid == 0:
                    continue
                else:
                    subprocess.run(cron_command, shell=True)
                    os._exit(pid)
        except Exception as exception:
            logging.warning(exception)
            sys.exit(1)

        time.sleep(constants.DEFAULT_SLEEP_INTERVAL)