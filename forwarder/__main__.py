import sys
import datetime
import logging
from forwarder import start
import config

logging.basicConfig(
    filename=config.FORWARDER["log_path"],
    filemode="a",
    level=logging.DEBUG,
    format="%(levelname)s:%(asctime)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    print(
        "\n---------- ----------- ----------\nTelegram Forwarder App by @Alvhix\n---------- ----------- ----------\n"
    )
    logger.info("Starting ForwarderApp")

    # initial variables
    start_time = datetime.datetime.now()
    if len(sys.argv) > 1:
        argument = str(sys.argv[1])
    else:
        argument = None
    logger.debug("Arguments given: " + str(argument))

    # start the program
    start(argument)

    logger.info(
        "Stopping ForwarderApp: executed for {}\n".format(
            datetime.datetime.now() - start_time
        )
    )
    sys.exit()


if __name__ == "__main__":
    main()