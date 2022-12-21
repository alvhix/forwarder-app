from os import path, environ
from dotenv import load_dotenv

load_dotenv()
_dirname = path.dirname(__file__)


class Config:
    """forwarder settings"""

    API_ID = int(environ.get("API_ID"))
    API_HASH = environ.get("API_HASH")
    RULES_PATH = environ.get(
        "RULES_PATH", path.join(_dirname, "forwarder-app.config.yml")
    )
    GROUP_MESSAGE = bool(
        environ.get("GROUP_MESSAGE", False)
    )  # True to group media messages before forwarding, (it may take $(periodicity_fwd) second/s to forward)
    PERIODICITY = int(
        environ.get("PERIODICITY", 1)
    )  # second/s (not used if $(group_messages) is false)
    TDJSON_VERBOSITY = int(environ.get("TDJSON_VERBOSITY", 1))
    LOG_FILE = environ.get("LOG_FILE", "log/app.log")
