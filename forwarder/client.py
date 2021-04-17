# Client low-level functions
from ctypes import CDLL, CFUNCTYPE, c_int, c_char_p, c_double
import sys
import json
import os
import config

# load shared library
tdjson = CDLL(config.CLIENT["tdlib_path"])

# load TDLib functions from shared library
_td_create_client_id = tdjson.td_create_client_id
_td_create_client_id.restype = c_int
_td_create_client_id.argtypes = []

_td_receive = tdjson.td_receive
_td_receive.restype = c_char_p
_td_receive.argtypes = [c_double]

_td_send = tdjson.td_send
_td_send.restype = None
_td_send.argtypes = [c_int, c_char_p]

_td_execute = tdjson.td_execute
_td_execute.restype = c_char_p
_td_execute.argtypes = [c_char_p]

fatal_error_callback_type = CFUNCTYPE(None, c_char_p)

_td_set_log_fatal_error_callback = tdjson.td_set_log_fatal_error_callback
_td_set_log_fatal_error_callback.restype = None
_td_set_log_fatal_error_callback.argtypes = [fatal_error_callback_type]

# initialize TDLib log with desired parameters
def on_fatal_error_callback(error_message):
    print("TDLib fatal error: ", error_message)
    sys.stdout.flush()


def td_execute(query):
    query = json.dumps(query).encode("utf-8")
    result = _td_execute(query)
    if result:
        result = json.loads(result.decode("utf-8"))
    return result


c_on_fatal_error_callback = fatal_error_callback_type(on_fatal_error_callback)
_td_set_log_fatal_error_callback(c_on_fatal_error_callback)

# setting TDLib log verbosity level to 1 (errors)
td_execute(
    {
        "@type": "setLogVerbosityLevel",
        "new_verbosity_level": 1,
        "@extra": 1.01234,
    }
)

# create client
client_id = _td_create_client_id()

# simple wrappers for client usage
def td_send(query):
    query = json.dumps(query).encode("utf-8")
    _td_send(client_id, query)


def td_receive():
    result = _td_receive(config.CLIENT["wait_timeout"])
    if result:
        result = json.loads(result.decode("utf-8"))
    return result


# send a message
def send_message(
    chat_id,
    message_thread_id,
    reply_to_message_id,
    options,
    reply_markup,
    input_message_content,
):
    td_send(
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
    chat_id, from_chat_id, messages_ids, options, send_copy, remove_caption
):
    td_send(
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