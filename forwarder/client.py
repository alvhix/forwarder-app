import json
import logging
from dotenv import load_dotenv
from forwarder.tdjson import TdJson


class Client:
    AUTHORIZATION = "updateAuthorizationState"
    WAIT_CODE = "authorizationStateWaitCode"
    WAIT_PASSWORD = "authorizationStateWaitPassword"
    WAIT_TDLIB_PARAMETERS = "authorizationStateWaitTdlibParameters"
    WAIT_ENCRYPTION_KEY = "authorizationStateWaitEncryptionKey"
    WAIT_PHONE_NUMBER = "authorizationStateWaitPhoneNumber"
    WAIT_REGISTRATION = "authorizationStateWaitRegistration"
    READY = "authorizationStateReady"
    CLOSING = "authorizationStateClosing"
    CLOSED = "authorizationStateClosed"
    NEW_MESSAGE = "updateNewMessage"
    ERROR = "error"
    SENDMESSAGE = "sendMessage"
    FORWARDMESSAGE = "forwardMessages"

    def __init__(
        self,
        api_id,
        api_hash,
        use_test_dc,
        tdlib_path,
        wait_timeout,
        database_directory,
        use_file_database,
        use_secret_chats,
        system_language,
        device_model,
        app_version,
        enable_storage_optimizer,
        verbosity,
    ) -> None:
        load_dotenv()
        self.logger = logging.getLogger(__name__)

        # initial parameters
        self.api_id = api_id
        self.api_hash = api_hash
        self.use_test_dc = use_test_dc
        self.wait_timeout = wait_timeout
        self.database_directory = database_directory
        self.use_file_database = use_file_database
        self.use_secret_chats = use_secret_chats
        self.system_language = system_language
        self.device_model = device_model
        self.app_version = app_version
        self.enable_storage_optimizer = enable_storage_optimizer
        self._tdjson = TdJson(tdlib_path, verbosity)
        self._tdjson.create_client()

    # simple wrappers for client usage
    def send(self, query) -> None:
        query = json.dumps(query).encode("utf-8")
        self._tdjson.send(self._tdjson.client, query)

    def receive(self) -> object:
        result = self._tdjson.receive(self._tdjson.client, self.wait_timeout)
        if result:
            result = json.loads(result.decode("utf-8"))
        return result

    def execute(self, query) -> object:
        query = json.dumps(query).encode("utf-8")
        result = self._tdjson.execute(self._tdjson.client, query)
        if result:
            result = json.loads(result.decode("utf-8"))
        return result

    def send_message(
        self,
        chat_id,
        message_thread_id,
        reply_to_message_id,
        options,
        reply_markup,
        input_message_content,
    ) -> None:
        self.send(
            {
                "@type": self.SENDMESSAGE,
                "chat_id": chat_id,
                "message_thread_id": message_thread_id,
                "reply_to_message_id": reply_to_message_id,
                "options": options,
                "reply_markup": reply_markup,
                "input_message_content": input_message_content,
            }
        )

    def forward_message(
        self, chat_id, from_chat_id, messages_ids, options, send_copy, remove_caption
    ) -> None:
        self.send(
            {
                "@type": self.FORWARDMESSAGE,
                "chat_id": chat_id,
                "from_chat_id": from_chat_id,
                "message_ids": messages_ids,
                "options": options,
                "send_copy": send_copy,
                "remove_caption": remove_caption,
            }
        )

    def stop(self) -> None:
        self._tdjson.destroy(self._tdjson.client)
