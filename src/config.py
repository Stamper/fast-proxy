from pathlib import Path

POOL_ID_HEADER = "X-POOL-ID"
REQUEST_ID_HEADER = "X-REQUEST-ID"
METHODS = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]
BASE_ROOT = Path(__file__).parent
TIMEOUT = .5
