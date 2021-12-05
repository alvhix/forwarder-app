import logging

from forwarder.client import Client
from forwarder.forwarder import Forwarder
from sys import exit
from config import CLIENT, FORWARDER
from datetime import datetime

logging.basicConfig(
    filename=FORWARDER["log_path"],
    filemode="a",
    level=FORWARDER["verbosity"],
    format="%(asctime)s [%(filename)s:%(lineno)d]|%(levelname)s|%(message)s",
)
logger = logging.getLogger(__name__)

# initial variables
start_time = datetime.now()
logger.info(f"Starting forwarder-app at {start_time}")

print(
    "---------- ----------- ----------\nTelegram Forwarder App by @Alvhix\n---------- ----------- ----------"
)

# build the client object
client = Client(
    CLIENT["api_id"],
    CLIENT["api_hash"],
    CLIENT["use_test_dc"],
    CLIENT["tdlib_path"],
    CLIENT["wait_timeout"],
    CLIENT["database_directory"],
    CLIENT["use_file_database"],
    CLIENT["use_secret_chats"],
    CLIENT["system_language"],
    CLIENT["device_model"],
    CLIENT["app_version"],
    CLIENT["enable_storage_optimizer"],
    CLIENT["verbosity"],
)

# build the forwarder object
forwarder = Forwarder(
    client,
    FORWARDER["limit_chats"],
    FORWARDER["periodicity_fwd"],
    FORWARDER["rules_path"],
    FORWARDER["log_path"],
    FORWARDER["group_messages"],
    FORWARDER["verbosity"],
)

# start the forwarder
forwarder.start()

logger.info(f"Stopping forwarder-app: executed for {datetime.now() - start_time}\n")
exit()
