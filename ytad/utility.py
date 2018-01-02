import logging
import json

_LOGGER = logging.getLogger(__name__)

def get_pretty_json(data):
    return json.dumps(
        data,
        sort_keys=True,
        indent=4,
        separators=(',', ': '))

def _json_normalizer(data, ignore_dicts = False):
    """Based on https://stackoverflow.com/a/33571117/706421 ."""

    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')

    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [
            _json_normalizer(item, ignore_dicts=True)
            for item
            in data
        ]

    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _json_normalizer(key, ignore_dicts=True):
                _json_normalizer(value, ignore_dicts=True)
            for key, value
            in data.items()
        }

    # if it's anything else, return it in its original form
    return data

def json_load_normal(f):
    """Parse JSON and only use Unicode strings if we have to.

    Based on https://stackoverflow.com/a/33571117/706421 .
    """

    return _json_normalizer(
        json.load(f, object_hook=_json_normalizer),
        ignore_dicts=True
    )

def json_loads_normal(raw):
    """Parse JSON and only use Unicode strings if we have to.

    Based on https://stackoverflow.com/a/33571117/706421 .
    """

    try:
        decoded = json.loads(raw, object_hook=_json_normalizer)
    except:
        _LOGGER.exception("Could not decode JSON:\n{}".format(raw))
        raise

    return _json_normalizer(
        decoded,
        ignore_dicts=True
    )
