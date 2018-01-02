import unittest

import ytad.accessor.playlists
import ytad.client_manager


class TestPlaylists(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.__cm = ytad.client_manager.get_client_manager()
        super(TestPlaylists, self).__init__(*args, **kwargs)

    def test_list_mine(self):
        p = ytad.accessor.playlists.Playlists(self.__cm)

        items = p.list_mine()
        items = list(items)

    def test_list_mine__return_content_details(self):
        p = ytad.accessor.playlists.Playlists(self.__cm)

        items = p.list_mine(return_content_details=True)
        items = list(items)
