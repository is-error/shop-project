from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from utils.response import Response
from utils.common import serializer_errors_response, exceptions_errors
from users.serializers.handle import LoginSerializer

# docs swaggers
import users.swaggers as swaggers


class LoginAPI(APIView):
    permission_classes = ()
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        tags=["Auth"],
        operation_id="API Đăng nhập",
        request_body=swaggers.auth_login_payload,
        operation_description="[POST] API Đăng nhập",
    )
    @exceptions_errors
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer_errors_response(serializer)
        login_result = serializer.login()
        return Response(result=login_result, msg="Đăng nhập thành công")
