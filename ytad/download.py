from __future__ import unicode_literals

import os
import logging
import time
import math

import youtube_dl

import ytad.client_manager
import ytad.poll
import ytad.accessor.playlists

_LOGGER = logging.getLogger(__name__)


class Download(object):
    def __init__(self, cm):
        self.__cm = cm

    def _download_one(self, download_path, video_id, title, print_output=True):
        """Download the video. youtube-dl will automatically resume any unfinished
        downloads.
        """

        filename = "%(upload_date)s - %(title)s (%(id)s).%(ext)s"
        filepath = os.path.join(download_path, filename)

        # By default, the mtime is set to the publish-date and confuses
        # absolutely everyone.
        options = {
            'quiet': True,
            'updatetime': False,
            'outtmpl': filepath,
        }

        start_epoch = time.time()

        with youtube_dl.YoutubeDL(options) as ydl:
            url = 'https://www.youtube.com/watch?v={}'.format(video_id)
            ydl.download([url])

        if print_output is True:
            duration_s = int(math.ceil(time.time() - start_epoch))
            print("- Download time: {}s".format(duration_s))

            # youtube-dl has some options to print JSON info, which should
            # presumably include a filename, but they don't work and/or aren't
            # sufficient.

            filenames = os.listdir(download_path)

            found = None
            for i, filename in enumerate(filenames):
                if filename[0] == '.':
                    continue

                if video_id in filename:
                    found = filename
                    break

            if found is None:
                for filename in sorted(os.listdir(download_path)):
                    _LOGGER.warning("FILE IN OUTPUT PATH: [{}]".format(filename))

                raise Exception("Could not find downloaded video: [{}]".format(video_id))

            filename = found

            print("- Filename: {}".format(filename))

            filepath = os.path.join(download_path, filename)
            s = os.stat(filepath)

            print("- Size: {:.1f}M".format(s.st_size / 1024.0 / 1024.0))

        return filepath

    def check_and_download(self, playlist_id, download_path=None, print_output=True):
        """Check for new videos and, optionally, download them."""

        if download_path is not None:
            if os.path.exists(download_path) is False:
                os.makedirs(download_path)

        p = ytad.poll.Poll(self.__cm, playlist_id)
        pa = None
        with p.new_songs() as new_songs:
            for song_identity in new_songs:
                if print_output is True:
                    if pa is None:
                        pa = ytad.accessor.playlists.Playlists(self.__cm)

                    playlist = pa.get_with_id(playlist_id)

                    print(song_identity.title)
                    print("- Playlist: {}".format(playlist.title))
                    print("- ID: {}".format(song_identity.video_id))

                if download_path is not None:
                    self._download_one(
                        download_path,
                        song_identity.video_id,
                        song_identity.title,
                        print_output=print_output)

                if print_output is True:
                    print('')
