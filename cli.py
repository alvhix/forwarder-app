from forwarder.client import Client
from forwarder.forwarder import Forwarder
import sys
import logging
from config import CLIENT, FORWARDER
from datetime import datetime

logging.basicConfig(
    filename=FORWARDER["log_path"],
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s [%(filename)s:%(lineno)d]|%(levelname)s|%(message)s",
)
logger = logging.getLogger(__name__)

# initial variables
start_time = datetime.now()
logger.info(f"Starting ForwarderApp at {start_time}")

print(
    "---------- ----------- ----------\nTelegram Forwarder App by @Alvhix\n---------- ----------- ----------"
)

# build the client object
client = Client(
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
)

# init the client with your api id and api hash
client.init_client(CLIENT["api_id"], CLIENT["api_hash"])

# build the forwarder object
forwarder = Forwarder(
    client,
    FORWARDER["limit_chats"],
    FORWARDER["periodicity_fwd"],
    FORWARDER["rules_path"],
    FORWARDER["log_path"],
    FORWARDER["group_messages"],
)

# start the forwarder
forwarder.start()

logger.info(f"Stopping ForwarderApp: executed for {datetime.now() - start_time}\n")
sys.exit()
