from ctypes import CDLL, CFUNCTYPE, c_int, c_char_p, c_double, c_void_p
from sys import exit
import logging


class TdJson:
    def __init__(self, tdlib_path, verbosity) -> None:
        self.logger = logging.getLogger(__name__)

        # load shared library
        _tdjson = CDLL(tdlib_path)

        # load TDLib functions from shared library
        self.create = _tdjson.td_json_client_create
        self.create.restype = c_void_p
        self.create.argtypes = []

        self.receive = _tdjson.td_json_client_receive
        self.receive.restype = c_char_p
        self.receive.argtypes = [c_void_p, c_double]

        self.send = _tdjson.td_json_client_send
        self.send.restype = None
        self.send.argtypes = [c_void_p, c_char_p]

        self.execute = _tdjson.td_json_client_execute
        self.execute.restype = c_char_p
        self.execute.argtypes = [c_void_p, c_char_p]

        self.destroy = _tdjson.td_json_client_destroy
        self.destroy.restype = None
        self.destroy.argtypes = [c_void_p]

        self.verbosity = _tdjson.td_set_log_verbosity_level
        self.verbosity.restype = None
        self.verbosity.argtypes = [c_int]

        # setting TDLib log verbosity level to 1
        self.verbosity(verbosity)

        fatal_error_callback_type = CFUNCTYPE(None, c_char_p)
        self.error_callback = _tdjson.td_set_log_fatal_error_callback
        self.error_callback.restype = None
        self.error_callback.argtypes = [fatal_error_callback_type]

        c_on_fatal_error_callback = fatal_error_callback_type(
            self.on_fatal_error_callback
        )
        self.error_callback(c_on_fatal_error_callback)

        self.client = self.create()

    def on_fatal_error_callback(self, message) -> None:
        self.logger.critical(message)
        exit()
