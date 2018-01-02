import logging
import json
import hashlib
import collections
import contextlib

import ytad.persisted
import ytad.accessor.playlist_items

_LOGGER = logging.getLogger(__name__)

_SONG_IDENTITY = \
    collections.namedtuple(
        '_SONG_IDENTITY', [
            'song_id',
            'video_id',
            'title',
        ])


class Poll(object):
    def __init__(self, cm, playlist_id):
        self.__playlist_id = playlist_id
        self.__cm = cm
        self.__p = ytad.persisted.Persisted()
        self.__pi = ytad.accessor.playlist_items.PlaylistItems(self.__cm)

    def _retrieve_songs(self):
        songs = self.__pi.list(self.__playlist_id)
        return songs

    @contextlib.contextmanager
    def new_songs(self):
        songs = self._retrieve_songs()
        identities = [(song.id, song.video_id, song.title) for song in songs]

        serialized = json.dumps(identities)
        current_hash_ = hashlib.sha1(serialized).hexdigest()

        current_metadata = {
            'songs': identities,
        }

        has_changed, _, recorded_metadata = \
            self.__p.has_changed(
                self.__playlist_id,
                current_hash_,
                current_metadata)

        if has_changed is False:
            _LOGGER.debug("No songs have changed. STATE=[{}]".format(
                          current_hash_))

            yield []
            return

        current_songs_s = set(identities)

        if recorded_metadata is None:
            recorded_songs_s = set()
        else:
            recorded_songs_s = set(recorded_metadata['songs'])

        new_songs_s = current_songs_s - recorded_songs_s
        if not new_songs_s:
            _LOGGER.debug("Songs were removed but not added.")
            yield []
            return

        new_identities = [
            _SONG_IDENTITY(*properties)
            for properties
            in new_songs_s
        ]

        identities_phrase = \
            '\n'.join([str(si) for si in new_identities])

        new_identities = sorted(new_identities)

        _LOGGER.debug("({}) new songs were found:\n{}".format(
                      len(new_songs_s), identities_phrase))

        yield new_identities

        # Only update if we got back successfully from whatever the caller was
        # doing.
        self.__p.set_playlist_state(
            self.__playlist_id,
            current_hash_,
            current_metadata)
