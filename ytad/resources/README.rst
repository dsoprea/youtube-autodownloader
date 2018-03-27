Overview
========

This tool knows how to poll for changes to playlist(s) and to then download the physical videos for the new items automatically (using `youtube-dl <https://github.com/rg3/youtube-dl>`_).


Features
========

- More than one playlist can be provided.
- The state is recorded for each playlist during each call. This is how the differences are calculated.
- Uses `python-googleautoauth <https://github.com/dsoprea/python-googleautoauth>`_ for authentication.
- Will gracefully accommodate multiple instances being run concurrently.


Installation
============

$ pip install youtube-autodownloader


Usage
=====

The first time you run, you will have to build new credentials. The automatic-authentication flow will automatically run and open a browser window. To specifically run just the authorization, run::

    $ ytad_autoauth

This works best in a desktop environment. Manual-authorization helper scripts are also provided to support console-only environment.


Since YouTube does not enforce uniqueness for playlist names, you are required to provide playlist IDs rather than names.

Example of finding a playlist ID using a playlist name::

    $ ytad_search_playlists Animals
    PLxaR7YEkaI0xxxxxxxxxxxxxxacWvmEih

    $ ytad_search_playlists Special
    PLxaR7YEkaI0xxxxxxxxxxxxxxr1gs86gE

Example of checking for and downloading new videos ("-p" is a playlist-ID, "-dp" is the download-path)::

    $ ytad_autodownload -p PLxaR7YEkaI0xxxxxxxxxxxxxxr1gs86gE -dp "/storage/videos/$(date '+\%Y')/Special"
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


Testing
=======

To run the tests::

    $ ./test.sh

The tests will require user interaction with the browser.


Notes
=====

- If you do not wish to download the videos the first time that you run this command, omit the download-path parameter. This will just build the local database. Otherwise, all videos from the playlist will download. This might not be desireable for your use-case.
