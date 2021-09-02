from ctypes import CDLL, CFUNCTYPE, c_int, c_char_p, c_double
import json
import config
from os import getenv
from dotenv import load_dotenv


class Client:
    def __init__(
        self,
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
    ) -> None:
        # initial parameters
        self.use_test_dc = use_test_dc
        self.tdlib_path = tdlib_path
        self.wait_timeout = wait_timeout
        self.database_directory = database_directory
        self.use_file_database = use_file_database
        self.use_secret_chats = use_secret_chats
        self.system_language = system_language
        self.device_model = device_model
        self.app_version = app_version
        self.enable_storage_optimizer = enable_storage_optimizer

        # load shared library
        tdjson = CDLL(self.tdlib_path)

        # load TDLib functions from shared library
        self._td_create_client_id = tdjson.td_create_client_id
        self._td_create_client_id.restype = c_int
        self._td_create_client_id.argtypes = []

        self._td_receive = tdjson.td_receive
        self._td_receive.restype = c_char_p
        self._td_receive.argtypes = [c_double]

        self._td_send = tdjson.td_send
        self._td_send.restype = None
        self._td_send.argtypes = [c_int, c_char_p]

        self._td_execute = tdjson.td_execute
        self._td_execute.restype = c_char_p
        self._td_execute.argtypes = [c_char_p]

        fatal_error_callback_type = CFUNCTYPE(None, c_char_p)

        self._td_set_log_fatal_error_callback = tdjson.td_set_log_fatal_error_callback
        self._td_set_log_fatal_error_callback.restype = None
        self._td_set_log_fatal_error_callback.argtypes = [fatal_error_callback_type]

    def init_client(self, api_id, api_hash):
        load_dotenv()

        # set api_id and api_hash
        if api_id is None:
            api_id = int(getenv("API_ID"))
        if api_hash is None:
            api_hash = str(getenv("API_HASH"))

        self.api_id = api_id
        self.api_hash = api_hash

        # setting TDLib log verbosity level to 1 (errors)
        self.td_execute(
            {
                "@type": "setLogVerbosityLevel",
                "new_verbosity_level": 1,
                "@extra": 1.01234,
            }
        )

        # create client
        self.client_id = self._td_create_client_id()

    # simple wrappers for client usage
    def td_send(self, query):
        query = json.dumps(query).encode("utf-8")
        self._td_send(self.client_id, query)

    def td_receive(self):
        result = self._td_receive(config.CLIENT["wait_timeout"])
        if result:
            result = json.loads(result.decode("utf-8"))
        return result

    def td_execute(self, query):
        query = json.dumps(query).encode("utf-8")
        result = self._td_execute(query)
        if result:
            result = json.loads(result.decode("utf-8"))
        return result

    # send a message
    def send_message(
        self,
        chat_id,
        message_thread_id,
        reply_to_message_id,
        options,
        reply_markup,
        input_message_content,
    ):
        self.td_send(
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
    ):
        self.td_send(
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
