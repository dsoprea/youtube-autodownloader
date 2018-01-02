import dateutil.parser

import ytad.entity._entity_base


class PlaylistItem(ytad.entity._entity_base.EntityBase):
    @property
    def id(self):
        return self.data['id']

    @property
    def title(self):
        return self.data['snippet']['title']

    @property
    def description(self):
        return self.data['snippet']['description']

    @property
    def published_at(self):
        return dateutil.parser.parse(self.data['snippet']['publishedAt'])

    @property
    def video_id(self):
        return self.data['snippet']['resourceId']['videoId']

    def __str__(self):
        return "PlaylistItem<ID=[{}] TITLE=[{}]>".format(self.id, self.title)
