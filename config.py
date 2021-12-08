from os import path, environ

_dirname = path.dirname(__file__)

""" forwarder settings """
FORWARDER = {
    "api_id": environ["API_ID"],
    "api_hash": environ["API_HASH"],
    "rules_path": path.join(_dirname, "forwarder-app.config.yml"),
    "periodicity_fwd": 1,  # second/s
    "group_messages": False,  # group media messages or not
    "verbosity": 1,
}
