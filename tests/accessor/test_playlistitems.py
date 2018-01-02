import unittest

import ytad.accessor.playlists
import ytad.accessor.playlist_items
import ytad.client_manager


class TestPlaylistItems(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.__cm = ytad.client_manager.get_client_manager()
        super(TestPlaylistItems, self).__init__(*args, **kwargs)

    def __get_first_nonempty_playlist(self):
        try:
            return self.__first_playlist_item
        except AttributeError:
            pass

        p = ytad.accessor.playlists.Playlists(self.__cm)

        playlists = p.list_mine(return_content_details=True)

        for playlist in playlists:
            if playlist.item_count > 0:
                self.__first_playlist_item = playlist
                return self.__first_playlist_item

        raise Exception("No non-empty playlists were found.")

    def test_list(self):
        item = self.__get_first_nonempty_playlist()

        p = ytad.accessor.playlist_items.PlaylistItems(self.__cm)

        songs = p.list(item.id)
        songs = list(songs)

        self.assertTrue(len(songs) > 0)
