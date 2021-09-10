import json
import logging
from ctypes import CDLL, CFUNCTYPE, c_int, c_char_p, c_double, c_void_p
from sys import exit
from os import getenv
from dotenv import load_dotenv


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
        _tdjson = CDLL(self.tdlib_path)

        # load TDLib functions from shared library
        self._td_json_client_create = _tdjson.td_json_client_create
        self._td_json_client_create.restype = c_void_p
        self._td_json_client_create.argtypes = []

        self._td_json_client_receive = _tdjson.td_json_client_receive
        self._td_json_client_receive.restype = c_char_p
        self._td_json_client_receive.argtypes = [c_void_p, c_double]

        self._td_json_client_send = _tdjson.td_json_client_send
        self._td_json_client_send.restype = None
        self._td_json_client_send.argtypes = [c_void_p, c_char_p]

        self._td_json_client_execute = _tdjson.td_json_client_execute
        self._td_json_client_execute.restype = c_char_p
        self._td_json_client_execute.argtypes = [c_void_p, c_char_p]

        self._td_json_client_destroy = _tdjson.td_json_client_destroy
        self._td_json_client_destroy.restype = None
        self._td_json_client_destroy.argtypes = [c_void_p]

        self._td_set_log_verbosity_level = _tdjson.td_set_log_verbosity_level
        self._td_set_log_verbosity_level.restype = None
        self._td_set_log_verbosity_level.argtypes = [c_int]

        # setting TDLib log verbosity level to 1
        self._td_set_log_verbosity_level(verbosity)

        fatal_error_callback_type = CFUNCTYPE(None, c_char_p)
        self._td_set_log_fatal_error_callback = _tdjson.td_set_log_fatal_error_callback
        self._td_set_log_fatal_error_callback.restype = None
        self._td_set_log_fatal_error_callback.argtypes = [fatal_error_callback_type]

        c_on_fatal_error_callback = fatal_error_callback_type(
            self.on_fatal_error_callback
        )
        self._td_set_log_fatal_error_callback(c_on_fatal_error_callback)

        # create client
        self._td_json_client = self._td_json_client_create()

    def on_fatal_error_callback(self, message) -> None:
        self.logger.critical(message)
        exit()

    # simple wrappers for client usage
    def send(self, query) -> None:
        query = json.dumps(query).encode("utf-8")
        self._td_json_client_send(self._td_json_client, query)

    def receive(self) -> object:
        result = self._td_json_client_receive(self._td_json_client, self.wait_timeout)
        if result:
            result = json.loads(result.decode("utf-8"))
        return result

    def execute(self, query) -> object:
        query = json.dumps(query).encode("utf-8")
        result = self._td_execute(self._td_json_client, query)
        if result:
            result = json.loads(result.decode("utf-8"))
        return result

    def stop(self) -> None:
        self._td_json_client_destroy(self._td_json_client)
