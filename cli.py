import logging
from config import Config
from forwarder.forwarder import Forwarder
from sys import exit
from datetime import datetime


logging.basicConfig(
    filename=Config.LOG_FILE,
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s [%(filename)s:%(lineno)d]|%(levelname)s|%(message)s",
)
logger = logging.getLogger(__name__)

# initial variables
start_time = datetime.now()
logger.info(f"Starting forwarder-app at {start_time}")

print(
    "\n---------- ----------- ----------\nTelegram Forwarder App by @Alvhix\n---------- ----------- ----------\n"
)

# build the forwarder object
forwarder = Forwarder(
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    rules_path=Config.RULES_PATH,
    periodicity_fwd=Config.PERIODICITY,
    group_messages=Config.GROUP_MESSAGE,
    verbosity=Config.TDJSON_VERBOSITY,
)

# start the forwarder
forwarder.start()

logger.info(f"Stopping forwarder-app: executed for {datetime.now() - start_time}\n")
exit()
