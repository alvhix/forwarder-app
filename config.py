from os import path, getenv
from dotenv import load_dotenv

load_dotenv()
__dirname = path.dirname(__file__)

""" client settings """
__lib = "lib/tdjson.dll"  # your tdjson .so or .dll file (depending on your OS)
CLIENT = {
    "use_test_dc": False,
    "tdlib_path": path.join(__dirname, __lib),
    "wait_timeout": 1,  # second/s
    "database_directory": "tdlib",
    "use_file_database": False,
    "use_chat_info_database": False,
    "use_message_database": False,
    "use_secret_chats": True,
    "api_id": int(getenv("API_ID")),  # your API_ID
    "api_hash": str(getenv("API_HASH")),  # your API_HASH
    "system_language": "en",
    "device_model": "Desktop",
    "app_version": "1.2",
    "enable_storage_optimizer": True,
}

""" forwarder settings """
FORWARDER = {
    "limit_chats": 5,  # don't put a bigger number of chats that you have
    "periodicity_fwd": 1,  # second/s
    "log_path": path.join(__dirname, "log/app.log"),
    "rules_path": path.join(__dirname, "rules.json"),
}
