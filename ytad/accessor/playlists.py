import logging

import ytad.entity_registry
import ytad.pager

_LOGGER = logging.getLogger(__name__)


class Playlists(object):
    def __init__(self, cm):
        self.__cm = cm

    @ytad.entity_registry.entity_response
    def _list_mine(self, parts=['id', 'snippet'], **kwargs):
        client = self.__cm.get_client()

        response = \
            client.playlists().list(
                mine=True,
                part=','.join(parts),
                **kwargs)

        return response

    def list_mine(self, return_content_details=False, **kwargs):
        if return_content_details is True:
            kwargs['parts'] = ['id', 'snippet', 'contentDetails']

        def cb(**kwargs2):
            kwargs.update(kwargs2)

            response = self._list_mine(**kwargs)
            return response

        return ytad.pager.all_items_gen(cb)

    @ytad.entity_registry.entity_response
    def _list_with_id(self, id, parts=['snippet']):
        client = self.__cm.get_client()

        response = \
            client.playlists().list(
                id=id,
                part=','.join(parts))

        return response

    def get_with_id(self, id):
        response = self._list_with_id(id)
        playlists = list(response.items)

        len_ = len(playlists)

        assert \
            0 < len_ < 2, \
            "Exactly one playlist was not found: COUNT=({}) ID=[{}]".format(
            len_, id)

        return playlists[0]
