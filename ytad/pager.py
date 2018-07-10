import logging

_LOGGER = logging.getLogger(__name__)

def all_items_gen(cb):
    page_token = None
    result_counter = None
    while 1:
        response = cb(pageToken=page_token)

        items = response.items
        items = list(items)

        if result_counter is None:
            result_counter = response.total_results

        result_counter -= len(items)

        for item in items:
            yield item

        if result_counter <= 0:
            break

        try:
            page_token = response.next_page_token
        except KeyError:
            break
