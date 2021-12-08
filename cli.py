import logging
from forwarder.forwarder import Forwarder
from config import FORWARDER
from sys import exit
from datetime import datetime


logging.basicConfig(
    filename="log/app.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s [%(filename)s:%(lineno)d]|%(levelname)s|%(message)s",
)
logger = logging.getLogger(__name__)

# initial variables
start_time = datetime.now()
logger.info(f"Starting forwarder-app at {start_time}")

print(
    "---------- ----------- ----------\nTelegram Forwarder App by @Alvhix\n---------- ----------- ----------"
)

# build the forwarder object
forwarder = Forwarder(
    FORWARDER["api_id"],
    FORWARDER["api_hash"],
    FORWARDER["rules_path"],
    FORWARDER["periodicity_fwd"],
    FORWARDER["group_messages"],
    FORWARDER["verbosity"],
)

# start the forwarder
forwarder.start()

logger.info(f"Stopping forwarder-app: executed for {datetime.now() - start_time}\n")
exit()
