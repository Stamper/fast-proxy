import logging
from logging.handlers import TimedRotatingFileHandler

import config

request_logger = logging.getLogger("requests")
request_logger.setLevel(logging.INFO)
response_logger = logging.getLogger("responses")
response_logger.setLevel(logging.INFO)
error_logger = logging.getLogger("errors")
error_logger.setLevel(logging.INFO)


formatter = logging.Formatter("%(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

requests_path = config.BASE_ROOT.parent / "logs" / "requests.log"
requests_file_handler = TimedRotatingFileHandler(
    filename=requests_path, when="midnight", backupCount=30
)
requests_file_handler.setFormatter(formatter)

response_path = config.BASE_ROOT.parent / "logs" / "responses.log"
response_file_handler = TimedRotatingFileHandler(
    filename=response_path, when="midnight", backupCount=30
)
response_file_handler.setFormatter(formatter)
response_file_handler.setLevel(logging.INFO)

error_path = config.BASE_ROOT.parent / "logs" / "errors.log"
errors_file_handler = TimedRotatingFileHandler(
    filename=error_path, when="midnight", backupCount=30
)
errors_file_handler.setFormatter(formatter)
errors_file_handler.setLevel(logging.INFO)

request_logger.addHandler(requests_file_handler)
response_logger.addHandler(response_file_handler)
error_logger.addHandler(errors_file_handler)

log_request = request_logger.info
log_response = response_logger.info
log_error = error_logger.info
