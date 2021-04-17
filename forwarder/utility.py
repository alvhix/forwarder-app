import json
import datetime
import logging
import config
from forwarder import client

logger = logging.getLogger(__name__)

# convert unix time in seconds to datetime and returns formatted datetime string
def convert_unix_to_datetime(unix):
    return (
        datetime.datetime.fromtimestamp(unix)
        .astimezone(tz=None)
        .strftime("%Y-%m-%d %H:%M:%S")
    )


# group message_id by rule_id
def group_message_id(messages):
    result = []
    for message in messages:
        if len(result) == 0:
            result.append(message)
        else:
            for index, row in enumerate(result):
                if row["rule_id"] == message["rule_id"]:
                    row["message_id"].extend(message["message_id"])
                    break
                else:
                    # if the is the last index
                    if index == len(result) - 1:
                        result.append(message)
                        break
    return result


# write in the events json log
def write_events(text):
    with open(config.FORWARDER["events_path"], "w") as events_log:
        events_log.write(json.dumps(text, indent=4))


# log api action
def log_api_action(chat_id, from_chat_id, message_id):
    text = (
        "Message/s with id: "
        + str(message_id)
        + " forwarded from: "
        + str(from_chat_id)
        + " to: "
        + str(chat_id)
    )
    logger.info(text)


# log api error
def log_api_error(event, type):
    text = "{} - {}".format(event["code"], event["message"])
    # check the error type
    if type == logging.ERROR:
        logger.error("Telegram API error: " + text)
    elif type == logging.CRITICAL:
        logger.critical("Telegram API critical error: " + text)