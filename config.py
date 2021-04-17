from os import path, environ

dirname = path.dirname(__file__)

""" client settings """
lib = "lib/libtdjson.so.1.7.1"  # your tdjson .so or .dll file (depending on your OS)
CLIENT = {
    "tdlib_path": path.join(dirname, lib),
    "wait_timeout": 0.5,  # second/s
    "database_directory": "tdlib",
    "use_message_database": True,
    "use_secret_chats": True,
    "api_id": int(environ["API_ID"]),  # your API_ID
    "api_hash": str(environ["API_HASH"]),  # your API_HASH
    "system_language": "es",
    "device_model": "Desktop",
    "app_version": "1.0",
    "enable_storage_optimizer": True,
}

""" forwarder settings """
FORWARDER = {
    "limit_chats": 5,  # don't put a bigger number of chats that you have
    "periodicity_fwd": 1,  # second/s
    "log_path": path.join(dirname, "log/app.log"),
    "events_path": path.join(dirname, "log/events.json"),
    "rules_path": path.join(dirname, "rules.json"),
}
