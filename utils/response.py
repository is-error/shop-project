from rest_framework.views import status, Response as views_response
from utils.status import get_status_name


class Response(views_response):
    def __init__(
        self,
        code=status.HTTP_200_OK,
        result=None,
        msg=None,
        error_msg=None,
        paginator=None,
        **extra_fields
    ):
        get_paginated_response = (
            paginator.get_paginated_response
            if hasattr(paginator, "get_paginated_response")
            else None
        )

        data = {
            "code": code,
            "msg": msg,
            "error_msg": error_msg,
            "data": result if paginator is None else get_paginated_response(result),
            "status": get_status_name(code),
        }

        data_extra_fields = {**extra_fields, **data}
        for key, value in data_extra_fields.items():
            data[key] = value
            if data_extra_fields[key] is None:
                data.pop(key)

        super(Response, self).__init__(
            data=data, status=status.HTTP_200_OK, **extra_fields
        )
