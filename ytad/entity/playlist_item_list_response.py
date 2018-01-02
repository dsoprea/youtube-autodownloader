import ytad.entity._list_base
import ytad.entity.playlist_item


class PlaylistItemListResponse(ytad.entity._list_base.ListBase):
    @property
    def items(self):
        for item in super(PlaylistItemListResponse, self).items:
            yield ytad.entity.playlist_item.PlaylistItem(item)
