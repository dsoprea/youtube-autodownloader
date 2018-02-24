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
    def __init__(self, cm, ytdl_username=None, ytdl_password=None, ytdl_twofactor=None):
        self.__cm = cm

        self.__username = os.environ.get('YTDL_USERNAME', ytdl_username)
        self.__password = os.environ.get('YTDL_PASSWORD', ytdl_password)
        self.__twofactor = os.environ.get('YTDL_TWOFACTOR', ytdl_twofactor)

    def _download_one(self, download_path, video_id, title, print_output=True):
        """Download the video. youtube-dl will automatically resume any unfinished
        downloads.
        """

        filename = "%(upload_date)s - " + title + " (%(id)s).%(ext)s"
        filepath = os.path.join(download_path, filename)

        marker_filename = '.' + video_id + '.marker'
        marker_filepath = os.path.join(download_path, marker_filename)

        if os.path.exists(marker_filepath) is True:
            s = os.stat(marker_filepath)
            age_s = int(time.time() - s.st_mtime)

            if age_s < 10 * 60:
                print("- SKIPPING! It may be downloading in a separate "
                      "process.")

                return

            os.remove(marker_filepath)

        _LOGGER.debug("Writing download marker: [{}]".format(marker_filepath))
        with open(marker_filepath, 'w'):
            pass

        try:
            # By default, the mtime is set to the publish-date and confuses
            # absolutely everyone.
            options = {
                'quiet': True,
                'updatetime': False,
                'outtmpl': filepath,
                'username': self.__username,
                'password': self.__password,
                'twofactor': self.__twofactor,
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
        finally:
            _LOGGER.debug("Removing download marker: [{}]".format(
                          marker_filepath))

            os.remove(marker_filepath)

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
                title = song_identity.title

                # Prune extended characters.

                i = 0
                while i < len(title):
                    if ord(title[i]) >= 0x80:
                        title = title[:i] + title[i + 1:]
                        continue

                    i += 1

                if print_output is True:
                    if pa is None:
                        pa = ytad.accessor.playlists.Playlists(self.__cm)

                    playlist = pa.get_with_id(playlist_id)

                    print(title)
                    print("- Playlist: {}".format(playlist.title))
                    print("- ID: {}".format(song_identity.video_id))

                if download_path is not None:
                    self._download_one(
                        download_path,
                        song_identity.video_id,
                        title,
                        print_output=print_output)

                if print_output is True:
                    print('')
