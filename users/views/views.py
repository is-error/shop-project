from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from utils.response import Response
from utils.common import exceptions_errors
from utils.pagination import CustomPagination
from users.serializers.views import LoginHistory, LoginHistorySerializer


class LoginHistoriesAPI(APIView):
    serializer_class = LoginHistorySerializer

    @swagger_auto_schema(
        tags=["Auth"],
        operation_id="API lịch sử đăng nhập",
        operation_description="[GET] API lịch sử đăng nhập",
    )
    @exceptions_errors
    def get(self, request, *args):
        paginator = CustomPagination()
        login_histories = LoginHistory.objects.filter(user=request.user).order_by("-id")
        paginate_query = paginator.paginate_queryset(login_histories, request)
        result = self.serializer_class(paginate_query, many=True).data
        return Response(result=result, paginator=paginator)
