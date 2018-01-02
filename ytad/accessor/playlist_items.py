import logging

import ytad.pager

_LOGGER = logging.getLogger(__name__)


class PlaylistItems(object):
    def __init__(self, cm):
        self.__cm = cm

    @ytad.entity_registry.entity_response
    def _list(self, id, **kwargs):
        client = self.__cm.get_client()

        options = {
            'maxResults': 25,
        }

        options.update(kwargs)

        response = \
            client.playlistItems().list(
                playlistId=id,
                part='id,snippet',
                **options)

        return response

    def list(self, id):
        def cb(**kwargs):
            response = self._list(id=id, **kwargs)
            return response

        return ytad.pager.all_items_gen(cb)
