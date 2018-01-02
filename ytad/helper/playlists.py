import logging

import ytad.accessor.playlists
import ytad.exceptions

_LOGGER = logging.getLogger(__name__)


class Playlists(object):
    def __init__(self, cm):
        self.__p = ytad.accessor.playlists.Playlists(cm)

    def find_all_in_mine(self, title):
        items = self.__p.list_mine()

        for item in items:
            if item.title != title:
                continue

            yield item

    def find_in_mine(self, title):
        """Return the first matching playlist.

        Note that playlist names are not guaranteed to be unique.
        """

        items = self.find_all_in_mine(title)
        for item in items:
            return item

        raise \
            ytad.exceptions.NotFoundException(
                "Playlist not found: [{}]".format(title))
