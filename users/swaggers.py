from drf_yasg import openapi

auth_login_payload = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    title="API Đăng nhập",
    description="API đăng nhập vào hệ thống",
    properties={
        "email": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Email đăng nhập",
            example="example@gexample.com",
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING, description="Mật khẩu", example="12345678"
        ),
    },
)
