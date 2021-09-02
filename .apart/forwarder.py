import json
import logging
from config import CLIENT, FORWARDER
from datetime import datetime
from getpass import getpass


class Forwarder:
    NEW_MESSAGE = "updateNewMessage"
    AUTHORIZATION = "updateAuthorizationState"
    ERROR = "error"

    def __init__(self, log_path, rules_path, periodicity_fwd, limit_chats) -> None:
        self.log_path = log_path
        self.rules_path = rules_path
        self.periodicity_fwd = periodicity_fwd
        self.limit_chats = limit_chats

    def start(self, client):
        logger = logging.getLogger(__name__)

        try:
            # load rules file
            rules_file = open(FORWARDER["rules_path"])
            rules = json.load(rules_file)

            # messages queue
            messages = []

            # chrono
            start_update_time = datetime.now()
            forwarded = 0

            # main events cycle
            while True:
                event = client.td_receive()
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
                            client.td_send(
                                {
                                    "@type": "setTdlibParameters",
                                    "parameters": {
                                        "database_directory": CLIENT[
                                            "database_directory"
                                        ],
                                        "use_message_database": CLIENT[
                                            "use_message_database"
                                        ],
                                        "use_secret_chats": CLIENT["use_secret_chats"],
                                        "api_id": CLIENT["api_id"],
                                        "api_hash": CLIENT["api_hash"],
                                        "system_language_code": CLIENT[
                                            "system_language"
                                        ],
                                        "device_model": CLIENT["device_model"],
                                        "application_version": CLIENT["app_version"],
                                        "enable_storage_optimizer": CLIENT[
                                            "enable_storage_optimizer"
                                        ],
                                    },
                                }
                            )

                        # set an encryption key for database to let know TDLib how to open the database
                        if auth_state["@type"] == "authorizationStateWaitEncryptionKey":
                            client.td_send(
                                {
                                    "@type": "checkDatabaseEncryptionKey",
                                    "encryption_key": "",
                                }
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
                            code = input(
                                "Please enter the authentication code you received: "
                            )
                            client.td_send(
                                {"@type": "checkAuthenticationCode", "code": code}
                            )

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
                                {
                                    "@type": "checkAuthenticationPassword",
                                    "password": password,
                                }
                            )

                    # handle an incoming update or an answer to a previously sent request
                    if event["@type"] == self.NEW_MESSAGE:
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
                                f"Message published at: {message['date']}, appended to the queue"
                            )
                            recently_added = True

                    if event["@type"] == self.ERROR:
                        # log the error
                        utility.log_api_error(event, logging.ERROR)

        except KeyboardInterrupt:
            logger.info("Listening to messages stopped: interrupted by user")
