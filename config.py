from os import path, environ

_dirname = path.dirname(__file__)

""" forwarder settings """
FORWARDER = {
    "api_id": environ["API_ID"],
    "api_hash": environ["API_HASH"],
    "rules_path": path.join(_dirname, "forwarder-app.config.yml"),
    "group_messages": False,  # True to group media messages before forwarding, (it may take $(periodicity_fwd) second/s to forward)
    "periodicity_fwd": 1,  # second/s (not used if $(group_messages) is false)
    "verbosity": 1,
}
