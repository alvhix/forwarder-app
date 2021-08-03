# Forwarder high-level functions
import json
import logging
import config
from datetime import datetime
from getpass import getpass
from forwarder import client
from forwarder import utility

logger = logging.getLogger(__name__)

# get user autorization
def user_authorization():
    have_authorization = False
    logger.debug("Starting user authorization")

    while not have_authorization:
        event = client.td_receive()
        if event:
            # process authorization states
            if event["@type"] == "updateAuthorizationState":
                auth_state = event["authorization_state"]

                # if client is closed, we need to destroy it and create new client
                if auth_state["@type"] == "authorizationStateClosed":
                    utility.log_api_error("authorizationStateClosed", logging.CRITICAL)
                    break

                # set TDLib parameters
                # you MUST obtain your own api_id and api_hash at https://my.telegram.org
                # and use them in the setTdlibParameters call
                if auth_state["@type"] == "authorizationStateWaitTdlibParameters":
                    client.td_send(
                        {
                            "@type": "setTdlibParameters",
                            "parameters": {
                                "database_directory": config.CLIENT[
                                    "database_directory"
                                ],
                                "use_message_database": config.CLIENT[
                                    "use_message_database"
                                ],
                                "use_secret_chats": config.CLIENT["use_secret_chats"],
                                "api_id": config.CLIENT["api_id"],
                                "api_hash": config.CLIENT["api_hash"],
                                "system_language_code": config.CLIENT[
                                    "system_language"
                                ],
                                "device_model": config.CLIENT["device_model"],
                                "application_version": config.CLIENT["app_version"],
                                "enable_storage_optimizer": config.CLIENT[
                                    "enable_storage_optimizer"
                                ],
                            },
                        }
                    )

                # set an encryption key for database to let know TDLib how to open the database
                if auth_state["@type"] == "authorizationStateWaitEncryptionKey":
                    client.td_send(
                        {"@type": "checkDatabaseEncryptionKey", "encryption_key": ""}
                    )

                # enter phone number to log in
                if auth_state["@type"] == "authorizationStateWaitPhoneNumber":
                    phone_number = input("Please enter your phone number: ")
                    client.td_send(
                        {
                            "@type": "setAuthenticationPhoneNumber",
                            "phone_number": phone_number,
                        }
                    )

                # wait for authorization code
                if auth_state["@type"] == "authorizationStateWaitCode":
                    code = input("Please enter the authentication code you received: ")
                    client.td_send({"@type": "checkAuthenticationCode", "code": code})

                # wait for first and last name for new users
                if auth_state["@type"] == "authorizationStateWaitRegistration":
                    first_name = input("Please enter your first name: ")
                    last_name = input("Please enter your last name: ")
                    client.td_send(
                        {
                            "@type": "registerUser",
                            "first_name": first_name,
                            "last_name": last_name,
                        }
                    )

                # wait for password if present
                if auth_state["@type"] == "authorizationStateWaitPassword":
                    password = getpass("Please enter your password: ")
                    client.td_send(
                        {"@type": "checkAuthenticationPassword", "password": password}
                    )

                if auth_state["@type"] == "authorizationStateReady":
                    have_authorization = True
                    logger.info("User authorized")

            if event["@type"] == "error":
                utility.log_api_error(event, logging.ERROR)

    return have_authorization


# start listening new messages to forward
def update_new_messages():
    try:
        rules_file = open(config.FORWARDER["rules_path"])
        rules = json.load(rules_file)
        # messages queue
        messages = []
        # chrono
        start_update_time = datetime.now()
        forwarded = 0

        print("Listening to new messages...")
        logger.info("Listening to new messages...")
        while True:
            recently_added = False
            event = client.td_receive()

            # event is not empty
            if event:
                # wait for a new message
                if event["@type"] == "updateNewMessage":
                    message = event["message"]
                    for rule in rules["forward"]:
                        # if the message from chat_id is not from an accepted source
                        if message["chat_id"] != rule["source"]:
                            continue

                        message_forward = {
                            "rule_id": rule["id"],
                            "message_id": [message["id"]],
                        }
                        # append the message to the queue
                        messages.append(message_forward)
                        logger.debug(
                            f"Message published at: {utility.convert_unix_to_datetime(message['date'])}, appended to the queue"
                        )
                        recently_added = True

                if event["@type"] == "error":
                    # log the error
                    utility.log_api_error(event, logging.ERROR)

            # proccess queue messages every x time
            now = datetime.now()
            difference_seconds = int((now - start_update_time).total_seconds())

            if difference_seconds % config.FORWARDER["periodicity_fwd"] == 0:
                # only execute this once
                if forwarded < difference_seconds:
                    # if a message was added in this iteration
                    if recently_added:
                        logger.warning(
                            "A recent message was added to the queue, skipping to next iteration"
                        )
                        # continue to the next iteration
                        continue

                    # there are messages to proccess
                    if len(messages) > 0:
                        logger.debug("Processing message queue")

                        # proccess stored messages
                        proccess_messages(messages, rules)

                        # clear queue of messages
                        messages.clear()
                        logger.debug("Message queue processed and cleared")

                    # updates forwarded state
                    forwarded = difference_seconds

    except KeyboardInterrupt:
        rules_file.close()
        logger.info("Listening to messages stopped: interrupted by user")


# forward stored messages in queue
def proccess_messages(messages, rules):
    grouped_messages = utility.group_message_id(messages)
    logger.debug("Message/s grouped by message_id")
    for message in grouped_messages:
        for rule in rules["forward"]:
            if message["rule_id"] == rule["id"]:
                # variables
                destination_ids = rule["destination"]
                source_id = rule["source"]
                message_id = message["message_id"]
                options = rule["options"]
                send_copy = rule["send_copy"]
                remove_caption = rule["remove_caption"]
                for chat_id in destination_ids:
                    # forward messages
                    client.forward_message(
                        chat_id,
                        source_id,
                        message_id,
                        options,
                        send_copy,
                        remove_caption,
                    )
                    # log action
                    utility.log_api_action(chat_id, source_id, message_id)


# main method
def start(argument=None):
    # start the client by sending request to it
    client.td_send({"@type": "getAuthorizationState", "@extra": 1.01234})
    # get authorization
    authorized = user_authorization()
    if authorized:
        is_closed = False
        while not is_closed:
            command = input(
                """
-> Enter command:
fwd - Start listening to new messages for forwarding
gcs - Get all chats from main chat list
l - Listen all updates/requests (for debugging)
q - Quit program
"""
            )

            if command == "fwd" or argument == "fwd":
                update_new_messages()
            elif command == "gcs" or argument == "gcs":
                chats_by_default = config.FORWARDER["limit_chats"]
                number_chats = input(
                    f"Enter the chats you want to retrieve ({chats_by_default} chats by default): "
                )
                if number_chats:
                    number_chats = int(number_chats)
                else:
                    number_chats = chats_by_default

                utility.get_chats(number_chats)
            elif command == "l" or argument == "l":
                utility.listen()
            elif command == "q":
                print("Stopping the execution...")
                is_closed = True
            else:
                pass
    else:
        logger.error("User not authorized")
