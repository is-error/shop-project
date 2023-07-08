from rest_framework import exceptions
from rest_framework.views import status
from utils.response import Response


def serializer_errors_response(serializer):
    if not serializer.is_valid():
        error_message = serializer.errors
        raise exceptions.APIException(error_message)


def exceptions_errors(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except exceptions.APIException as error:
            return Response(error_msg=error.detail, code=status.HTTP_400_BAD_REQUEST)

    return wrapper
