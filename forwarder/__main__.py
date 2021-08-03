import sys
import logging
import config

from datetime import datetime
from forwarder import start

logging.basicConfig(
    filename=config.FORWARDER["log_path"],
    filemode="a",
    level=logging.INFO,
    format="%(levelname)s:%(asctime)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    print(
        """---------- ----------- ----------
Telegram Forwarder App by @Alvhix
---------- ----------- ----------"""
    )
    logger.info("Starting ForwarderApp")

    # initial variables
    start_time = datetime.now()
    if len(sys.argv) > 1:
        argument = str(sys.argv[1])
    else:
        argument = None
    logger.debug(f"Arguments given: {str(argument)}")

    # start the program
    start(argument)

    logger.info(f"Stopping ForwarderApp: executed for {datetime.now() - start_time}\n")
    sys.exit()


if __name__ == "__main__":
    main()
