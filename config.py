import platform
from os import path, environ
from dotenv import load_dotenv

load_dotenv()
__dirname = path.dirname(__file__)

""" client settings """
if platform.system() == "Windows":
    if platform.architecture()[0] == '64bit':
        __lib = "lib/windows/amd64/tdjson.dll"
elif platform.system() == "Linux":
    if platform.architecture()[0] == '64bit':
        __lib = "lib/linux/amd64/libtdjson.so"

CLIENT = {
    "api_id": environ["API_ID"],  # your API_ID
    "api_hash": environ["API_HASH"],  # your API_HASH
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
    "verbosity": 1,
}

""" forwarder settings """
FORWARDER = {
    "limit_chats": 100000,
    "periodicity_fwd": 1,  # second/s
    "log_path": path.join(__dirname, "log/app.log"),
    "rules_path": path.join(__dirname, "forwarder-app.config.yml"),
    "group_messages": False,  # group media messages or not
}
