"""
Common reusable Parameters classes
----------------------------------
"""
from flask import url_for

from flask_restplus import reqparse

pagination_param = reqparse.RequestParser()
pagination_param.add_argument('offset', type=int, required=False, default=1,
                              help='starting point in result set')

pagination_param.add_argument('limit', type=int, required=False,
                              choices=[2, 4, 6, 8, 10, 20],
                              default=2, help='Results per page {error_msg}')


class PaginationHelper(object):

    def __init__(self, query, resource_for_url, key_name, schema, limit, offset):
        self.query = query
        self.resource_for_url = resource_for_url
        self.key_name = key_name
        self.schema = schema
        self.page_size = limit
        self.offset = offset

    def paginate_query(self):

        # If no page number is specified, we assume the request requires page #1
        page_number = self.offset
        paginated_objects = self.query.paginate(page_number, per_page=self.page_size, error_out=False)
        objects = paginated_objects.items
        if paginated_objects.has_prev:
            previous_page_url = url_for(self.resource_for_url, page=page_number - 1, _external=True)
        else:
            previous_page_url = None
        if paginated_objects.has_next:
            next_page_url = url_for(self.resource_for_url, page=page_number + 1, _external=True)
        else:
            next_page_url = None
        dumped_objects = self.schema.dump(obj=objects, many=True)
        return ({self.key_name: dumped_objects, 'previous': previous_page_url,
                 'next': next_page_url, 'count': paginated_objects.total})
