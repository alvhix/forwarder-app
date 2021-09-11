import yaml
import logging
import sys
from forwarder.message import Message
from datetime import datetime
from getpass import getpass


class Forwarder:
    def __init__(
        self, client, limit_chats, periodicity_fwd, rules_path, log_path, group_messages
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.client = client
        self.rules_path = rules_path
        self.log_path = log_path
        self.periodicity_fwd = periodicity_fwd
        self.limit_chats = limit_chats
        self.group_messages = group_messages

        # load rules file
        with open(self.rules_path) as rules_file:
            self.rules = yaml.full_load(rules_file)["forward"]
            self.logger.info(f"Rules loaded: {self.rules}")

        # forwarder variables
        self.forwarded = 0
        self.messages = []
        self.start_update_time = 0

    def __str__(self) -> str:
        return (
            "{"
            + f"client: {self.client}, log_path: {self.log_path}, rules_path: {self.rules_path}, log_path: {self.log_path}, periodicity_fwd: {self.periodicity_fwd}, limit_chats: {self.limit_chats}"
            + "}"
        )

        # send a message

    def send_message(
        self,
        chat_id,
        message_thread_id,
        reply_to_message_id,
        options,
        reply_markup,
        input_message_content,
    ) -> None:
        self.client.send(
            {
                "@type": "sendMessage",
                "chat_id": chat_id,
                "message_thread_id": message_thread_id,
                "reply_to_message_id": reply_to_message_id,
                "options": options,
                "reply_markup": reply_markup,
                "input_message_content": input_message_content,
            }
        )

    # forward messages
    def forward_message(
        self, chat_id, from_chat_id, messages_ids, options, send_copy, remove_caption
    ) -> None:
        self.client.send(
            {
                "@type": "forwardMessages",
                "chat_id": chat_id,
                "from_chat_id": from_chat_id,
                "message_ids": messages_ids,
                "options": options,
                "send_copy": send_copy,
                "remove_caption": remove_caption,
            }
        )

    def start(self) -> None:
        # start the client by sending request to it
        self.client.send({"@type": "getAuthorizationState"})

        # chrono
        self.start_update_time = datetime.now()
        try:
            # main events cycle
            while True:
                self.recently_added = False
                event = self.client.receive()

                if event:
                    # authenticate user
                    self.authenticate_user(event)

                    # handle new messages
                    self.new_message_update_handler(event)

                    # handler errors
                    self.error_update_handler(event)

                    # handle every update
                    self.listen_update_handler(event)

                # process the message queue (if is not empty)
                self.process_message_queue()

        except KeyboardInterrupt:
            self.client.stop()
            self.logger.info("Client destroyed by the user")

    # login
    def authenticate_user(self, event) -> None:
        # process authorization states
        if event["@type"] == self.client.AUTHORIZATION:
            auth_state = event["authorization_state"]

            # if client is closed, we need to destroy it and create new client
            if auth_state["@type"] == self.client.CLOSED:
                self.logger.critical(event)
                raise ValueError(event)

            # set TDLib parameters
            # you MUST obtain your own api_id and api_hash at https://my.telegram.org
            # and use them in the setTdlibParameters call
            if auth_state["@type"] == self.client.WAIT_TDLIB_PARAMETERS:
                self.client.send(
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
            if auth_state["@type"] == self.client.WAIT_ENCRYPTION_KEY:
                self.client.send(
                    {
                        "@type": "checkDatabaseEncryptionKey",
                        "encryption_key": "",
                    }
                )

            # enter phone number to log in
            if auth_state["@type"] == self.client.WAIT_PHONE_NUMBER:
                phone_number = input("Please enter your phone number: ")
                self.client.send(
                    {
                        "@type": "setAuthenticationPhoneNumber",
                        "phone_number": phone_number,
                    }
                )

            # wait for authorization code
            if auth_state["@type"] == self.client.WAIT_CODE:
                code = input("Please enter the authentication code you received: ")
                self.client.send({"@type": "checkAuthenticationCode", "code": code})

            # wait for first and last name for new users
            if auth_state["@type"] == self.client.WAIT_REGISTRATION:
                first_name = input("Please enter your first name: ")
                last_name = input("Please enter your last name: ")
                self.client.send(
                    {
                        "@type": "registerUser",
                        "first_name": first_name,
                        "last_name": last_name,
                    }
                )

            # wait for password if present
            if auth_state["@type"] == self.client.WAIT_PASSWORD:
                password = getpass("Please enter your password: ")
                self.client.send(
                    {
                        "@type": "checkAuthenticationPassword",
                        "password": password,
                    }
                )

            # user authenticated
            if auth_state["@type"] == self.client.READY:
                # get all chats
                self.client.send({"@type": "getChats", "limit": self.limit_chats})
                self.logger.debug("User authorized")

    # handle new messages updates
    def new_message_update_handler(self, event) -> None:
        # handle incoming messages
        if event["@type"] == self.client.NEW_MESSAGE:
            message_update = event["message"]

            for rule in self.rules:
                # if the message from chat_id is not from an defined source
                if message_update["chat_id"] != rule["source"]:
                    continue

                # build the message
                message = Message(message_update, rule)

                # group messages or not
                if self.group_messages:
                    # append the message to the queue
                    self.messages.append(message)
                    self.recently_added = True
                    self.logger.debug("Message appended to the queue")
                else:
                    self.process_message(message)

    # log error
    def error_update_handler(self, event) -> None:
        if event["@type"] == self.client.ERROR:
            # log the error
            self.logger.error(event)

    # log events
    def listen_update_handler(self, event):
        self.logger.debug(str(event).encode())
        sys.stdout.flush()

    # forward the message
    def process_message(self, message) -> None:
        # variables
        message_id = message.message_id
        source_id = message.source_id
        destination_ids = message.destination_ids
        options = message.options
        send_copy = message.send_copy
        remove_caption = message.remove_caption
        for chat_id in destination_ids:
            # forward messages
            self.forward_message(
                chat_id,
                source_id,
                message_id,
                options,
                send_copy,
                remove_caption,
            )
            # log action
            self.logger.info(f"Message forwarding has been sent to the API: {message}")
            print(f"Message forwarded: {message}")

    # process grouped messages
    def process_message_queue(self) -> None:
        # there are messages to proccess
        if self.messages:
            # proccess queue messages
            self.difference_seconds = int(
                (datetime.now() - self.start_update_time).total_seconds()
            )

            if self.difference_seconds % self.periodicity_fwd == 0:
                # only execute this once every x seconds
                if self.forwarded < self.difference_seconds:
                    # message added recently, skip to next iteration
                    if not self.recently_added:
                        self.logger.debug("Processing message queue")

                        # proccess stored messages
                        grouped_messages = self.group_message_id(self.messages)
                        self.logger.debug("Message/s grouped by rule_id")

                        for message in grouped_messages:
                            self.process_message(message)

                        # clear queue of messages
                        self.messages.clear()
                        self.logger.debug("Message queue processed and cleared")

                    # updates forwarded state
                    self.forwarded = self.difference_seconds

    # group message_id by rule_id
    def group_message_id(self, messages) -> list:
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
