from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"

    @property
    def current_page(self):
        page_string = self.request.query_params.get(self.page_query_param, 1)
        return int(page_string) if str(page_string).isnumeric() else 1

    def get_paginated_response(self, data):
        return {
            "results": data,
            "page": self.current_page,
            "page_size": self.page_size,
            "count": self.page.paginator.count,
            "num_pages": self.page.paginator.num_pages,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
        }
