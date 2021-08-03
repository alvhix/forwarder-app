import json
import datetime
import logging
import config
from pprint import pprint
from forwarder import client

logger = logging.getLogger(__name__)

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


# convert unix time in seconds to datetime and returns formatted datetime string
def convert_unix_to_datetime(unix):
    return (
        datetime.datetime.fromtimestamp(unix)
        .astimezone(tz=None)
        .strftime("%Y-%m-%d %H:%M:%S")
    )


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
    text = f"{event['code']} - {event['message']}"
    # check the error type
    if type == logging.ERROR:
        logger.error("Telegram API error: " + text)
    elif type == logging.CRITICAL:
        logger.critical("Telegram API critical error: " + text)


# get chats from main chat list
def get_chats(limit_chats):
    print("Getting main chat list...")
    logging.info("Getting main chat list")

    chat_list = {"chat_list": []}
    # send request to the Telegram API
    client.td_send({"@type": "getChats", "limit": limit_chats})
    while len(chat_list["chat_list"]) < limit_chats:
        event = client.td_receive()
        if event:
            if event["@type"] == "updateNewChat":
                chat_list["chat_list"].append(event)

    # write in the events file
    write_events(chat_list)
    logger.info("Got main chat list, check log/events.json")


# listen all requests/updates and writes in a file (for debugging)
def listen():
    try:
        print("Listening all requests/updates...")
        logger.debug("Listening all requests/updates")
        event_list = []

        while True:
            event = client.td_receive()
            if event:
                event_list.append(event)
                pprint(event)

    except KeyboardInterrupt:
        write_events(event_list)
        logger.info("Listening all requests/updates stopped: interrupted by user")
