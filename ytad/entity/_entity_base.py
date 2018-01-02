import ytad.utility


class EntityBase(object):
    def __init__(self, data):
        self.__data = data

    @property
    def data(self):
        return self.__data

    @property
    def kind(self):
        return self.__data['kind']

    @property
    def etag(self):
        return self.__data['etag']

    def __str__(self):
        return 'Entity<{}>'.format(self.__data['kind'])

    def __repr__(self):
        return ytad.utility.get_pretty_json(self.__data)
