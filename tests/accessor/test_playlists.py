import unittest

import ytad.accessor.playlists
import ytad.client_manager


class TestPlaylists(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.__cm = ytad.client_manager.get_client_manager()
        super(TestPlaylists, self).__init__(*args, **kwargs)

    def __get_first_playlist(self):
        try:
            return self.__first_playlist_item
        except AttributeError:
            pass

        p = ytad.accessor.playlists.Playlists(self.__cm)

        playlists = p.list_mine()

        for playlist in playlists:
            return playlist

        raise Exception("No non-empty playlists were found.")

    def test_list_mine(self):
        p = ytad.accessor.playlists.Playlists(self.__cm)

        items = p.list_mine()
        items = list(items)

    def test_list_mine__return_content_details(self):
        p = ytad.accessor.playlists.Playlists(self.__cm)

        items = p.list_mine(return_content_details=True)
        items = list(items)

    def test_get_with_id(self):
        playlist = self.__get_first_playlist()

        p = ytad.accessor.playlists.Playlists(self.__cm)
        recovered = p.get_with_id(playlist.id)

        self.assertEquals(recovered.id, playlist.id)
