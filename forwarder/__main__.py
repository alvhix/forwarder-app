from forwarder.client import Client
from forwarder.forwarder import Forwarder
import sys
import logging
from config import CLIENT, FORWARDER
from datetime import datetime

logging.basicConfig(
    filename=FORWARDER["log_path"],
    filemode="a",
    level=logging.DEBUG,
    format="%(asctime)s [%(filename)s:%(lineno)d]|%(levelname)s|%(message)s",
)
logger = logging.getLogger(__name__)


def main():
    print(
        "---------- ----------- ----------\nTelegram Forwarder App by @Alvhix\n---------- ----------- ----------"
    )

    # initial variables
    start_time = datetime.now()
    logger.info(f"Starting ForwarderApp at {start_time}")

    if len(sys.argv) > 1:
        argument = str(sys.argv[1])
    else:
        argument = None
    logger.debug(f"Arguments given: {str(argument)}")

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
        FORWARDER["limit_chats"],
        FORWARDER["periodicity_fwd"],
        FORWARDER["log_path"],
        FORWARDER["rules_path"],
        client,
    )
    logger.debug(f"Forwarder object: {forwarder}")

    # start the forwarder
    forwarder.start()

    logger.info(f"Stopping ForwarderApp: executed for {datetime.now() - start_time}\n")
    sys.exit()


if __name__ == "__main__":
    main()
