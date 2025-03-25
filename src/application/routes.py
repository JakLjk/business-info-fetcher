import uuid
import time
import os
import logging
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify

from src.business_info_fetcher import scrape_krs_api
from src.business_info_fetcher import scrape_krs_dokumenty_finansowe_document_list
from src.application.queues import queue_krs_api, queue_krs_dokumenty_finansowe
from src.log import setup_logger


setup_logger("ROUTES_LOG", "ROUTES_LOG")
route_log = logging.getLogger("ROUTES_LOG")
route_log.info("Queue initialisation log initialised.")

route_log.info("Initialising flask blueprints")
webhook_bp = Blueprint('webhook', __name__)

timeout =int(os.getenv("SERVER_SCRAPE_RESPONSE_TIMEOUT"))

@webhook_bp.route("/get-krs-api-json", methods=["GET"])
def webhook_get_krs_api():
    route_log.info("Received request to get KRS API JSON")
    type_of_report = request.args.get("type_of_report")
    krs_number = request.args.get("krs_number")
    stance_string = request.args.get("stance_string")
    route_log.info(f"Request parameters: \
                   type_of_report: {type_of_report}, \
                    krs_number: {krs_number}, \
                    stance_string: {stance_string}")

    route_log.info("Enqueuing job to scrape KRS API")
    job_id = str(uuid.uuid4())
    job = queue_krs_api.enqueue(
        scrape_krs_api,
        args=(type_of_report, krs_number, stance_string),
        job_id=job_id
    )
    
    route_log.info(f"Job {job_id} enqueued")
    t=0
    while not job.is_finished:
        t+=1
        if job.is_failed:
            route_log.error(f"Job {job_id} failed", str(job.exc_info))
            return jsonify({"status": "Job failed", "details": str(job.exc_info)}), 500
        if t>timeout:
            route_log.error(f"Job {job_id} timeout")
            return jsonify({"status": "Job timeout"}), 408
        time.sleep(1)
        job.refresh()

    route_log.info(f"Job {job_id} finished")
    return jsonify({"status": "Job finished", "result": job.result}), 200

@webhook_bp.route("/get-krs-dokumenty-finansowe-document-list", methods=["GET"])
def webhook_get_krs_dokumenty_finansowe_document_list():
    route_log.info("Received request to get KRS API JSON")
    krs = request.args.get("krs")
    route_log.info(f"Request parameters: \
                krs_number: {krs}")

    route_log.info("Enqueuing job to scrape krs document list")
    job_id = str(uuid.uuid4())
    job = queue_krs_dokumenty_finansowe.enqueue(
        scrape_krs_dokumenty_finansowe_document_list,
        args=(krs,),
        job_id=job_id
    )
    route_log.info(f"Job {job_id} enqueued")
    t=0
    while not job.is_finished:
        t+=1
        if job.is_failed:
            route_log.error(f"Job {job_id} failed", str(job.exc_info))
            return jsonify({"status": "Job failed", "details": str(job.exc_info)}), 500
        if t>timeout:
            route_log.error(f"Job {job_id} timeout")
            return jsonify({"status": "Job timeout"}), 408
        time.sleep(1)
        job.refresh()

    route_log.info(f"Job {job_id} finished")
    return jsonify({"status":"Job finished", "result":job.result})