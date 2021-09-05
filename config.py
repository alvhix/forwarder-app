from platform import system
from os import path, getenv
from dotenv import load_dotenv

load_dotenv()
__dirname = path.dirname(__file__)

""" client settings """
if system() == "Windows":
    __lib = "lib\\windows\\tdjson.dll"
elif system() == "Linux":
    __lib = "lib\\linux\\libtdjson.so.1.7.4"

CLIENT = {
    "api_id": int(getenv("API_ID")),  # your API_ID
    "api_hash": str(getenv("API_HASH")),  # your API_HASH
    "use_test_dc": False,
    "tdlib_path": path.join(__dirname, __lib),
    "wait_timeout": 1,  # second/s
    "database_directory": "tdlib",
    "use_file_database": False,
    "use_chat_info_database": False,
    "use_message_database": False,
    "use_secret_chats": True,
    "system_language": "en",
    "device_model": "Desktop",
    "app_version": "0.1.0",
    "enable_storage_optimizer": True,
}

""" forwarder settings """
FORWARDER = {
    "limit_chats": 9223372036854775807, # 2 ^ 63 -1
    "periodicity_fwd": 1,  # second/s
    "log_path": path.join(__dirname, "log\\app.log"),
    "rules_path": path.join(__dirname, "forwarder-app.config.yml"),
    "group_messages": False,  # group media messages or not
}
