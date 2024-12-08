"""Launch app using uvicorn web server"""

import logging

import uvicorn

from app import app

LOG_LEVEL = logging.INFO

if __name__ == "__main__":
    logging.basicConfig(level=LOG_LEVEL)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=LOG_LEVEL)
