import argparse
import os 

from dotenv import load_dotenv
from redis import Redis
from rq import Worker
import logging

from src.log import setup_logger

load_dotenv()

ACCEPTED_QUERE_ARGS = ["queue_krs_api", "queue_krs_dokumenty_finansowe"]


def main():
    setup_logger("WORKER_LOG", "WORKER_LOG")
    work_log = logging.getLogger("WORKER_LOG")
    work_log.info("Initialising worker")

    work_log.info("Reading command line arguments")
    parser = argparse.ArgumentParser(description="Select worker queue to be initialised.")
    parser.add_argument(
    "--queue_names", 
    nargs='+',
    choices=ACCEPTED_QUERE_ARGS,
    required=True, 
    help="Start worker listening on provided queues."
    )
    args = parser.parse_args()

    work_log.info("Initialising connection with redis")
    work_log.info(f"Redis server address: {os.getenv("REDIS_URL")}")
    queue_names = args.queue_names
    redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
    work_log.info("Checking connection with redis server")
    try:
        work_log.debug(redis_conn.ping())
    except ConnectionError as ce:
        raise ce
    work_log.info(f"Starting worker in queues: {queue_names}")
    worker = Worker(queue_names, connection=redis_conn)
    worker.work()


if __name__ == "__main__":
    main()