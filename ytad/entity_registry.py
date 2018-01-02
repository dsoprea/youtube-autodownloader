import contextlib

import ytad.entity.playlist_response

KIND_MAP = {
    'youtube#playlistListResponse':
        ytad.entity.playlist_response.PlaylistResponse,
}

def factory(data):
    cls = KIND_MAP[data['kind']]
    return cls(data)

def entity_response(f):
    """Client method decorator to automatically translate responses into
    entities.
    """

    def wrapper(self, *args, **kwargs):
        request = f(self, *args, **kwargs)
        response = request.execute()

        entity = factory(response)
        return entity

    return wrapper
