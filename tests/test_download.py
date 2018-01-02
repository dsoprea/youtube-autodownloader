import unittest

import ytad.download
import ytad.client_manager
import ytad.test_support
import ytad.accessor.playlists


class TestDownload(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.__cm = ytad.client_manager.get_client_manager()
        super(TestDownload, self).__init__(*args, **kwargs)

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

    def test_download_one(self):
        with ytad.test_support.temp_path() as path:
            d = ytad.download.Download(self.__cm)
            d._download_one(
                path,
                'Y0NxxZWMOMQ',
                "Double Squirrel Assault Course",
                print_output=False)

    def test_check_and_download(self):
        with ytad.test_support.temp_path() as path:
            playlist = self.__get_first_nonempty_playlist()

            d = ytad.download.Download(self.__cm)
            d.check_and_download(playlist.id, print_output=False)
