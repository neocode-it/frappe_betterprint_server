import logging
import os

def setup_logger():
    log_directory = "/var/log/betterprint_server"
    log_file = os.path.join(log_directory, "worker.log")

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logging.basicConfig(
        filename=log_file,
        level=logging.ERROR,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log(exc):
    setup_logger()
    logging.exception("Exception occurred: ", exc_info=exc)
