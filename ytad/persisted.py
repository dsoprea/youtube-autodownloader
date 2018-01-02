import os
import logging
import pickle
import datetime

import dateutil.parser

import ytad.config.persisted

_LOGGER = logging.getLogger(__name__)


class Persisted(object):
    def __init__(self, filepath=None):
        if filepath is None:
            filepath = \
                os.environ.get(
                    'YTAD_STATE_FILEPATH',
                    ytad.config.persisted.DEFAULT_STATE_FILEPATH)

        filepath = os.path.expanduser(filepath)

        path = os.path.dirname(filepath)
        if os.path.exists(path) is False:
            os.makedirs(path)

        _LOGGER.debug("State filepath: [{}]".format(filepath))
        self.__filepath = filepath

    @property
    def _state(self):
        try:
            return self.__state
        except AttributeError:
            pass

        if os.path.exists(self.__filepath) is False:
            self.__state = {}
        else:
            with open(self.__filepath) as f:
                self.__state = pickle.load(f)

        return self.__state

    def get_playlist_state(self, id_):
        return self._state[id_]

    def has_changed(self, id_, current_hash_, current_metadata, allow_update=False):
        try:
            x = self._state[id_]
        except KeyError:
            x = None

        if x is None:
            if allow_update is True:
                self.set_playlist_state(id_, current_hash_, current_metadata)

            return True, None, None

        recorded_hash_, recorded_timestamp_phrase, recorded_metadata = x
        recorded_timestamp_dt = dateutil.parser.parse(recorded_timestamp_phrase)

        now_dt = datetime.datetime.now()

        has_changed = current_hash_ != recorded_hash_

        if has_changed and allow_update is True:
            self.set_playlist_state(id_, current_hash_, current_metadata)

        return \
            has_changed, \
            (now_dt - recorded_timestamp_dt), \
            recorded_metadata

    def set_playlist_state(self, id_, hash_, metadata):
        now_dt = datetime.datetime.now()
        timestamp_phrase = now_dt.isoformat()

        self._state[id_] = (hash_, timestamp_phrase, metadata)

        with open(self.__filepath, 'w') as f:
            pickle.dump(self._state, f)

        del self.__state
