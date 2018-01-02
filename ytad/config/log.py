import os
import logging

_DEBUG_RAW = os.environ.get('DEBUG', '0')
_IS_DEBUG = _DEBUG_RAW == 'true' or _DEBUG_RAW == '1'
_DEFAULT_LOG_LEVEL_NAME = os.environ.get('LOG_LEVEL_NAME', 'WARNING')

_LOGGER = logging.getLogger(__name__)

def configure(is_debug=_IS_DEBUG, default_level_name=_DEFAULT_LOG_LEVEL_NAME):
    """Configure logging. Note that our default level is so restrictive because
    we might be printing JSON data and we don't want to disrupt that for
    anything but actual errors.
    """

    if is_debug is True:
        level = logging.DEBUG
    else:
        level = getattr(logging, default_level_name)

    logger = logging.getLogger()

    logger.setLevel(level)

    sh = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(name)s %(levelname)s] %(message)s')
    sh.setFormatter(formatter)
    logger.addHandler(sh)
