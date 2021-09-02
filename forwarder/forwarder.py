import json
import logging
from forwarder.message import Message
from config import CLIENT, FORWARDER
from datetime import datetime
from getpass import getpass


class Forwarder:
    NEW_MESSAGE = "updateNewMessage"
    AUTHORIZATION = "updateAuthorizationState"
    ERROR = "error"

    def __init__(
        self, limit_chats, periodicity_fwd, rules_path, log_path, client
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.log_path = log_path
        self.rules_path = rules_path
        self.periodicity_fwd = periodicity_fwd
        self.limit_chats = limit_chats
        self.client = client

    def start(self):
        # start the client by sending request to it
        self.client.td_send({"@type": "getAuthorizationState", "@extra": 1.01234})

        # load rules file
        rules_file = open(FORWARDER["rules_path"])
        rules = json.load(rules_file)

        # messages queue
        messages = []

        # chrono
        start_update_time = datetime.now()
        forwarded = 0
        try:
            # main events cycle
            while True:
                recently_added = False
                event = self.client.td_receive()

                if event:
                    # process authorization states
                    if event["@type"] == self.AUTHORIZATION:
                        auth_state = event["authorization_state"]

                        # if client is closed, we need to destroy it and create new client
                        if auth_state["@type"] == "authorizationStateClosed":
                            break

                        # set TDLib parameters
                        # you MUST obtain your own api_id and api_hash at https://my.telegram.org
                        # and use them in the setTdlibParameters call
                        if (
                            auth_state["@type"]
                            == "authorizationStateWaitTdlibParameters"
                        ):
                            self.client.td_send(
                                {
                                    "@type": "setTdlibParameters",
                                    "parameters": {
                                        "database_directory": self.client.database_directory,
                                        "use_file_database": self.client.use_file_database,
                                        "use_secret_chats": self.client.use_secret_chats,
                                        "api_id": self.client.api_id,
                                        "api_hash": self.client.api_hash,
                                        "system_language_code": self.client.system_language,
                                        "device_model": self.client.device_model,
                                        "application_version": self.client.app_version,
                                        "enable_storage_optimizer": self.client.enable_storage_optimizer,
                                    },
                                }
                            )

                        # set an encryption key for database to let know TDLib how to open the database
                        if auth_state["@type"] == "authorizationStateWaitEncryptionKey":
                            self.client.td_send(
                                {
                                    "@type": "checkDatabaseEncryptionKey",
                                    "encryption_key": "",
                                }
                            )

                        # enter phone number to log in
                        if auth_state["@type"] == "authorizationStateWaitPhoneNumber":
                            phone_number = input("Please enter your phone number: ")
                            self.client.td_send(
                                {
                                    "@type": "setAuthenticationPhoneNumber",
                                    "phone_number": phone_number,
                                }
                            )

                        # wait for authorization code
                        if auth_state["@type"] == "authorizationStateWaitCode":
                            code = input(
                                "Please enter the authentication code you received: "
                            )
                            self.client.td_send(
                                {"@type": "checkAuthenticationCode", "code": code}
                            )

                        # wait for first and last name for new users
                        if auth_state["@type"] == "authorizationStateWaitRegistration":
                            first_name = input("Please enter your first name: ")
                            last_name = input("Please enter your last name: ")
                            self.client.td_send(
                                {
                                    "@type": "registerUser",
                                    "first_name": first_name,
                                    "last_name": last_name,
                                }
                            )

                        # wait for password if present
                        if auth_state["@type"] == "authorizationStateWaitPassword":
                            password = getpass("Please enter your password: ")
                            self.client.td_send(
                                {
                                    "@type": "checkAuthenticationPassword",
                                    "password": password,
                                }
                            )

                    # handle incoming updates or an answer to a previously sent request
                    if event["@type"] == self.NEW_MESSAGE:
                        message_update = event["message"]

                        # first, get all chats
                        self.client.td_send({"@type": "getChats", "limit": 10000})

                        for rule in rules["forward"]:
                            # if the message from chat_id is not from an accepted source
                            if message_update["chat_id"] != rule["source"]:
                                continue
                            message = Message(
                                [message_update["id"]],
                                message_update["chat_id"],
                                message_update["date"],
                                rule["id"],
                            )

                            # append the message to the queue
                            messages.append(message)
                            self.logger.debug(
                                f"Message {message}, appended to the queue"
                            )
                            recently_added = True

                    if event["@type"] == self.ERROR:
                        # log the error
                        self.logger.error(event)

                # proccess queue messages
                now = datetime.now()
                difference_seconds = int((now - start_update_time).total_seconds())

                if difference_seconds % FORWARDER["periodicity_fwd"] == 0:
                    # only execute this once every x seconds
                    if forwarded < difference_seconds:
                        # message added recently, skip to next iteration
                        if recently_added:
                            self.logger.warning(
                                "A recent message was added to the queue, skipping to next iteration"
                            )
                            continue

                        # there are messages to proccess
                        if messages:
                            self.logger.debug("Processing message queue")

                            # proccess stored messages
                            self.proccess_messages(messages, rules)

                            # clear queue of messages
                            messages.clear()
                            self.logger.debug("Message queue processed and cleared")

                        # updates forwarded state
                        forwarded = difference_seconds

        except KeyboardInterrupt:
            self.logger.info("Listening to messages stopped: interrupted by user")

    # forward stored messages in queue
    def proccess_messages(self, messages, rules):
        grouped_messages = self.group_message_id(messages)
        self.logger.debug("Message/s grouped by rule_id")

        for message in grouped_messages:
            for rule in rules["forward"]:
                if message.rule_id == rule["id"]:
                    # variables
                    destination_ids = rule["destination"]
                    source_id = rule["source"]
                    message_id = message.message_id
                    options = rule["options"]
                    send_copy = rule["send_copy"]
                    remove_caption = rule["remove_caption"]
                    for chat_id in destination_ids:
                        # forward messages
                        self.client.forward_message(
                            chat_id,
                            source_id,
                            message_id,
                            options,
                            send_copy,
                            remove_caption,
                        )
                        # log action
                        self.logger.info(f"Message forwarding has been sent to the API")
                        print(f"Message forwarded: {message}")

    # group message_id by rule_id
    def group_message_id(self, messages):
        result = []
        for message in messages:
            if not result:
                result.append(message)
            else:
                for index, row in enumerate(result):
                    if row.rule_id == message.rule_id:
                        row.message_id.extend(message.message_id)
                        break
                    else:
                        # if is the last index
                        if index == len(result) - 1:
                            result.append(message)
                            break
        return result
