import logging
from cron import get_cron_tasks, run_cron, get_cron
import constants


def init():
    logging.basicConfig(filename='cron.log', filemode='a', level=logging.DEBUG,
                        format='%(asctime)s.%(msecs)03d:%(name)s:%(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info("starting")
    logging.info("getting cron tasks")

    get_cron(constants.CRONTAB_PATH)
    get_cron_tasks()

    try:
        run_cron()
    except KeyboardInterrupt:
        logging.info("close cron tasks")


if __name__ == '__main__':
    init()