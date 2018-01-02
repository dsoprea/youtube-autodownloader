import unittest

import ytad.accessor.playlists
import ytad.helper.playlists
import ytad.client_manager


class TestPlaylists(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.__cm = ytad.client_manager.get_client_manager()
        super(TestPlaylists, self).__init__(*args, **kwargs)

    def __get_first_playlist_name(self):
        try:
            return self.__first_playlist_item
        except AttributeError:
            pass

        p = ytad.accessor.playlists.Playlists(self.__cm)

        items = p.list_mine()
        item = next(items)

        self.__first_playlist_item = item
        return self.__first_playlist_item

    def test_find_all_in_mine(self):
        existing_item = self.__get_first_playlist_name()

        p = ytad.helper.playlists.Playlists(self.__cm)

        items = p.find_all_in_mine(existing_item.title)
        items = list(items)

        self.assertTrue(len(items) > 0)

    def test_find_in_mine(self):
        existing_item = self.__get_first_playlist_name()

        p = ytad.helper.playlists.Playlists(self.__cm)

        item = p.find_in_mine(existing_item.title)
        self.assertEquals(item.id, existing_item.id)
