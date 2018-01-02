import logging

import ytad.entity_registry

_LOGGER = logging.getLogger(__name__)


class Playlists(object):
    def __init__(self, cm):
        self.__cm = cm

    @ytad.entity_registry.entity_response
    def _list_mine(self, **kwargs):
        client = self.__cm.get_client()

        response = \
            client.playlists().list(
                mine=True,
                part='id,snippet',
                **kwargs)

        return response

    def list_mine(self):
        page_token = None
        result_counter = None
        while 1:
            kwargs = {}
            if page_token is not None:
                kwargs['pageToken'] = page_token

            response = self._list_mine(**kwargs)

            items = response.items
            items = list(items)

            if result_counter is None:
                result_counter = response.total_results

            result_counter -= len(items)

            for item in items:
                yield item

            if result_counter <= 0:
                break

            page_token = response.next_page_token
