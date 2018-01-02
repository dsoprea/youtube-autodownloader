import ytad.entity._entity_base


class ListBase(ytad.entity._entity_base.EntityBase):
    @property
    def next_page_token(self):
        return self.data['nextPageToken']

    @property
    def items(self):
        return self.data['items']

    @property
    def results_per_page(self):
        return self.data['pageInfo']['resultsPerPage']

    @property
    def total_results(self):
        return self.data['pageInfo']['totalResults']
