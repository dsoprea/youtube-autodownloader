import ytad.entity._list_base
import ytad.entity.playlist


class PlaylistResponse(ytad.entity._list_base.ListBase):
    @property
    def items(self):
        for item in super(PlaylistResponse, self).items:
            yield ytad.entity.playlist.Playlist(item)
