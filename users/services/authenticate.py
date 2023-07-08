from django.contrib.auth.backends import BaseBackend
from rest_framework import exceptions

from users.models.user import User


class Mybackend(BaseBackend):
    def authenticate(self, **kwargs):
        try:
            user = User.objects.get(
                **{User.USERNAME_FIELD: kwargs[User.USERNAME_FIELD]}
            )
        except User.DoesNotExist:
            raise exceptions.APIException(
                {
                    User.USERNAME_FIELD: "{} does not exist".format(
                        User.USERNAME_FIELD.capitalize()
                    )
                }
            )

        is_correct = user.check_password(kwargs["password"])
        if not is_correct:
            raise exceptions.APIException({"password": "Invalid password"})
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
