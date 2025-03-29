import os
from dotenv import load_dotenv
from redis import Redis
from rq import Worker, Queue
from src.log import setup_logger
import logging

load_dotenv()

setup_logger("QUEUE_INIT_LOG", "QUEUE_INIT_LOG")
queue_log = logging.getLogger("QUEUE_INIT_LOG")
queue_log.info("Queue initialisation log initialised.")

queue_log.info("Initialising connection with redis")
queue_log.info(f"Redis server address:  {os.getenv('REDIS_URL')}")
redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
queue_log.info("Checking connection with redis server")
try:
    redis_conn.ping()
except ConnectionError as ce:
    raise ce
queue_log.info("Connection with redis server established")
queue_log.info("Initialising queues")
timeout = int(os.getenv("RQ_WORKER_TIMEOUT"))
queue_log.info(f"Setting queue job value timeout to: {timeout}")
queue_krs_api = Queue('queue_krs_api',
                      connection=redis_conn, 
                      default_timeout=timeout)
queue_krs_dokumenty_finansowe = Queue('queue_krs_dokumenty_finansowe', 
                                      connection=redis_conn, 
                                      default_timeout=timeout)
queue_log.info("Queues initialised")
