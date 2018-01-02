import ytad.entity._list_base
import ytad.entity.playlist


class PlaylistListResponse(ytad.entity._list_base.ListBase):
    @property
    def items(self):
        for item in super(PlaylistListResponse, self).items:
            yield ytad.entity.playlist.Playlist(item)
