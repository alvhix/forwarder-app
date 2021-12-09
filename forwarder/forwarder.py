import yaml
import logging
from pywtdlib.client import Client
from pywtdlib.enum import Update
from forwarder.message import Message
from datetime import datetime


class Forwarder:
    def __init__(
        self,
        api_id,
        api_hash,
        rules_path,
        periodicity_fwd,
        group_messages,
        verbosity,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.api_id = api_id
        self.api_hash = api_hash
        self.rules_path = rules_path
        self.periodicity_fwd = periodicity_fwd
        self.group_messages = group_messages
        self.verbosity = verbosity

        # load rules file
        with open(self.rules_path) as rules_file:
            self.rules = yaml.full_load(rules_file)["forward"]
            self.logger.info(f"Rules loaded: {self.rules}")

        # forwarder variables
        self.forwarded = 0
        self.messages = []
        self.start_update_time = datetime.now()

    def new_message_update_handler(self, event) -> None:
        # handle incoming messages
        if event["@type"] == Update.NEW_MESSAGE:
            message_update = event["message"]

            for rule in self.rules:
                # if the message from chat_id is not from an defined source
                if message_update["chat_id"] != rule["source"]:
                    continue

                # build the message
                message = Message(message_update, rule)

                # process message with the configured options
                self.get_option(message)

    def get_option(self, message):
        if self.group_messages:
            self.messages.append(message)
            self.recently_added = True
            self.logger.debug("Message appended to the queue")
        else:
            self.forward_messages(message)

    def forward_messages(self, message) -> None:
        message_id = message.message_id
        source_id = message.source_id
        destination_ids = message.destination_ids
        options = message.options
        send_copy = message.send_copy
        remove_caption = message.remove_caption

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
            self.logger.info(f"Message has been sent to the API: {message}")

    def process_grouped_messages(self) -> None:
        # there are messages to proccess
        if self.messages:
            # proccess queue messages
            self.difference_seconds = int(
                (datetime.now() - self.start_update_time).total_seconds()
            )

            # only execute this once every x seconds
            if self.difference_seconds % self.periodicity_fwd == 0:
                if self.forwarded < self.difference_seconds:
                    # message added recently, skip to next iteration
                    if not self.recently_added:
                        self.logger.debug("Processing message queue")

                        # proccess stored messages
                        grouped_messages = self.group_message_id(self.messages)
                        self.logger.debug("Message/s grouped by rule_id")

                        for message in grouped_messages:
                            self.forward_messages(message)

                        # clear queue of messages
                        self.messages.clear()
                        self.logger.debug("Message queue processed and cleared")

                # updates forwarded state
                self.forwarded = self.difference_seconds

        self.recently_added = False

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

    def start(self):
        self.client = Client(
            api_id=self.api_id, api_hash=self.api_hash, verbosity=self.verbosity
        )

        self.client.set_update_handler(self.new_message_update_handler)
        self.client.set_routine_handler(self.process_grouped_messages)

        self.client.start()
