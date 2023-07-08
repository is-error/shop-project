from rest_framework.views import exception_handler, status
from utils.status import get_status_name


def ExceptionHandler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            "code": response.status_code,
            "status": get_status_name(response.status_code),
        }
        response.status_code = status.HTTP_200_OK
    return response
