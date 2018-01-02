import logging

import ytad.pager
import ytad.entity_registry

_LOGGER = logging.getLogger(__name__)


class PlaylistItems(object):
    def __init__(self, cm):
        self.__cm = cm

    @ytad.entity_registry.entity_response
    def _list(self, playlist_id, **kwargs):
        client = self.__cm.get_client()

        options = {
            'maxResults': 25,
        }

        options.update(kwargs)

        response = \
            client.playlistItems().list(
                playlistId=playlist_id,
                part='id,snippet',
                **options)

        return response

    def list(self, playlist_id):
        def cb(**kwargs):
            response = self._list(playlist_id, **kwargs)
            return response

        return ytad.pager.all_items_gen(cb)
