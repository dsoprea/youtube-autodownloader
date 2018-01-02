import os
import unittest

import ytad.client_manager
import ytad.poll
import ytad.test_support
import ytad.accessor.playlists


class TestPoll(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.__cm = ytad.client_manager.get_client_manager()
        super(TestPoll, self).__init__(*args, **kwargs)

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

    def test_new_songs(self):
        class Song(object):
            def __init__(self, song_id, video_id, title):
                self.id = song_id
                self.video_id = video_id
                self.title = title

        class TestPollNoSongs(ytad.poll.Poll):
            def _retrieve_songs(self):
                return [
                ]

        class TestPollOriginalSongs(ytad.poll.Poll):
            def _retrieve_songs(self):
                return [
                    Song('SONG-ID-1', 'VIDEO-ID-1', 'TITLE-1'),
                    Song('SONG-ID-2', 'VIDEO-ID-2', 'TITLE-2'),
                    Song('SONG-ID-3', 'VIDEO-ID-3', 'TITLE-3'),
                ]

        class TestPollNewSongs(ytad.poll.Poll):
            def _retrieve_songs(self):
                return [
                    Song('SONG-ID-1', 'VIDEO-ID-1', 'TITLE-1'),
                    Song('SONG-ID-2', 'VIDEO-ID-2', 'TITLE-2'),
                    Song('SONG-ID-3', 'VIDEO-ID-3', 'TITLE-3'),
                    Song('SONG-ID-4', 'VIDEO-ID-4', 'TITLE-4'),
                    Song('SONG-ID-5', 'VIDEO-ID-5', 'TITLE-5'),
                ]

        with ytad.test_support.temp_path() as path:
            filepath = os.path.join(path, 'state')

            with ytad.test_support.environment(
                    YTAD_STATE_FILEPATH=filepath):

                # Start out with a so-called "empty" playlist.

                p = TestPollNoSongs(self.__cm, 'PLAYLIST-ID')
                with p.new_songs() as no_songs:
                    expected = []
                    self.assertEquals(no_songs, expected)

                # Now, introduce an original set of songs.

                p = TestPollOriginalSongs(self.__cm, 'PLAYLIST-ID')
                with p.new_songs() as original_songs:
                    expected = [
                        ytad.poll._SONG_IDENTITY(song_id='SONG-ID-1', video_id='VIDEO-ID-1', title='TITLE-1'),
                        ytad.poll._SONG_IDENTITY(song_id='SONG-ID-2', video_id='VIDEO-ID-2', title='TITLE-2'),
                        ytad.poll._SONG_IDENTITY(song_id='SONG-ID-3', video_id='VIDEO-ID-3', title='TITLE-3'),
                    ]

                    self.assertEquals(original_songs, expected)

                # Now, add some more.

                p = TestPollNewSongs(self.__cm, 'PLAYLIST-ID')
                with p.new_songs() as new_songs:
                    expected = [
                        ytad.poll._SONG_IDENTITY(song_id='SONG-ID-4', video_id='VIDEO-ID-4', title='TITLE-4'),
                        ytad.poll._SONG_IDENTITY(song_id='SONG-ID-5', video_id='VIDEO-ID-5', title='TITLE-5'),
                    ]

                    self.assertEquals(new_songs, expected)

    def test_new_songs__live(self):
        with ytad.test_support.temp_path() as path:
            filepath = os.path.join(path, 'state')

            with ytad.test_support.environment(
                    YTAD_STATE_FILEPATH=filepath):

                item = self.__get_first_nonempty_playlist()

                p = ytad.poll.Poll(self.__cm, item.id)
                with p.new_songs() as songs:
                    self.assertTrue(len(songs) > 0)

    def test_new_songs__no_update_on_exception(self):
        class Song(object):
            def __init__(self, song_id, video_id, title):
                self.id = song_id
                self.video_id = video_id
                self.title = title

        class TestPoll(ytad.poll.Poll):
            def _retrieve_songs(self):
                return [
                    Song('SONG-ID-1', 'VIDEO-ID-1', 'TITLE-1'),
                    Song('SONG-ID-2', 'VIDEO-ID-2', 'TITLE-2'),
                    Song('SONG-ID-3', 'VIDEO-ID-3', 'TITLE-3'),
                ]

        with ytad.test_support.temp_path() as path:
            filepath = os.path.join(path, 'state')

            with ytad.test_support.environment(
                    YTAD_STATE_FILEPATH=filepath):

                try:
                    p = TestPoll(self.__cm, 'PLAYLIST-ID')
                    with p.new_songs() as no_songs:
                        raise Exception("ERROR!")
                except Exception as e:
                    if str(e) != 'ERROR!':
                        raise
                else:
                    raise Exception("Expected exception from yield block.")

            self.assertFalse(os.path.exists(filepath))
