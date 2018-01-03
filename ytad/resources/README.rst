Overview
========

This tool knows how to poll for changes to playlist(s) and to then download the physical videos for the new items automatically (using `youtube-dl <https://github.com/rg3/youtube-dl>`_).


Features
========

- More than one playlist can be provided.
- The state is recorded for each playlist during each call. This is how the differences are calculated.
- Uses `python-googleautoauth <https://github.com/dsoprea/python-googleautoauth>`_ for authentication.
- Will gracefully accommodate multiple instances being run concurrently.


Usage
=====

Since YouTube does not enforce uniqueness for playlist names, you are required to provide playlist IDs rather than names.

Example of finding a playlist ID using a playlist name::

    $ ytad_search_playlists Animals
    PLxaR7YEkaI0xop_lzMT6BxAPGacWvmEih

    $ ytad_search_playlists Special
    PLxaR7YEkaI0yLK521mTCd4kqHr1gs86gE

Example of checking for and downloading new videos ("-p" is a playlist-ID, "-dp" is the download-path)::

    $ ytad_autodownload -p PLxaR7YEkaI0yLK521mTCd4kqHr1gs86gE -dp "/storage/videos/$(date '+\%Y')/Special"
    Lion Vs Mongoose: Mongoose Fends Off Four Lions
    - Playlist: Special
    - ID: 1TPn1-SJqVM
    - Download time: 9s
    - Filename: 20140902 - Lion Vs Mongoose - Mongoose Fends Off Four Lions (1TPn1-SJqVM).mp4
    - Size: 22.1M

    Slow loris loves getting tickled http://bit.ly/14qLq8x
    - Playlist: Special
    - ID: PZ5ACLVjYwM
    - Download time: 3s
    - Filename: 20090426 - Slow loris loves getting tickled http -_bit.ly_14qLq8x (PZ5ACLVjYwM).webm
    - Size: 3.1M


Notes
=====

- If you do not wish to download all videos in a playlist the first time that you run this command, omit the download-path parameter.
