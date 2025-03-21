from typing import Literal
from redis import Redis
from rq import Worker, Queue, Connection


def add_worker_to_queue(worker_name:Literal["worker_scrape_krs_api"]):
    redis_conn = Redis(host='redis', port=6379)
    if worker_name == "worker_scrape_krs_api":
        defined_queue = Queue('krs_api_queue', connection=redis_conn)

    with Connection(redis_conn):
        worker = Worker([defined_queue])
        worker.work()