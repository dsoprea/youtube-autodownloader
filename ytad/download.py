from __future__ import unicode_literals

import os
import logging
import time
import math

import youtube_dl

import ytad.client_manager
import ytad.poll

_LOGGER = logging.getLogger(__name__)


class Download(object):
    def __init__(self, cm):
        self.__cm = cm

    def _download_one(self, download_path, video_id, title, print_output=True):
        """Download the video. youtube-dl will automatically resume any unfinished
        downloads.
        """

        original_filenames = os.listdir(download_path)

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

        duration_s = int(math.ceil(time.time() - start_epoch))

        if print_output is True:
            print("- Download time: {}s".format(duration_s))

        current_filenames = os.listdir(download_path)
        new_filenames_s = set(current_filenames) - set(original_filenames)

        found = None
        for filename in new_filenames_s:
            if video_id in filename:
                found = filename
                break

        assert \
            found is not None, \
            "Could not find downloaded video: [{}]".format(video_id)

        filename = found

        if print_output is True:
            print("- Filename: {}".format(filename))

        filepath = os.path.join(download_path, filename)
        s = os.stat(filepath)

        if print_output is True:
            print("- Size: {:.1f}M".format(s.st_size / 1024.0 / 1024.0))

        return filepath

    def check_and_download(self, playlist_id, download_path=None, print_output=True):
        """Check for new videos and, optionally, download them."""

        if download_path is not None:
            if os.path.exists(download_path) is False:
                os.makedirs(download_path)

        p = ytad.poll.Poll(self.__cm, playlist_id)
        with p.new_songs() as new_songs:
            for song_identity in new_songs:
                if print_output is True:
                    print(song_identity.title)
                    print("- ID: {}".format(song_identity.video_id))

                if download_path is not None:
                    self._download_one(
                        download_path,
                        song_identity.video_id,
                        song_identity.title,
                        print_output=print_output)

                if print_output is True:
                    print('')
