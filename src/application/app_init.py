import logging
import os
from dotenv import load_dotenv
from redis import Redis
from rq import Worker, Queue
from flask import Flask

from src.log import setup_logger
from src.application.routes import webhook_bp


def main():
    setup_logger("SERVER_LOG", "SERVER_LOG")
    main_log = logging.getLogger("SERVER_LOG")
    main_log.info("Server log initialised.")

    main_log.info("Initialising Flask App")
    app = Flask(__name__)
    app.register_blueprint(webhook_bp)

    main_log.info("Running flask app...")
    app.run(host='0.0.0.0',port=5001, debug=True)


if __name__ == "__main__":
    main()
