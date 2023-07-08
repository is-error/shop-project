from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction

from users.models import User, LoginHistory
from users.services.authenticate import Mybackend

from ip2geotools.databases.noncommercial import DbIpCity
import requests


class CustomTokenObtainSerializer(TokenObtainSerializer):
    def parse_ip_address(self, ip_address):
        response = DbIpCity.get(ip_address, api_key="free")
        return {
            "location": f"{response.city}, {response.region}, {response.country}",
            "latitude": response.latitude,
            "longitude": response.longitude,
        }

    def save_login_history(self, user_logged):
        ipify_requests = requests.get("https://api.ipify.org")
        ip_address = ipify_requests.content.decode("utf8")
        parse_data = self.parse_ip_address(ip_address)
        LoginHistory.objects.create(
            user=user_logged,
            ip_address=ip_address,
            location=parse_data["location"],
            latitude=parse_data["latitude"],
            longitude=parse_data["longitude"],
        )

    @transaction.atomic
    def validate(self, attrs):
        authenticate_kwargs = {
            User.USERNAME_FIELD: attrs[User.USERNAME_FIELD],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = Mybackend.authenticate(self, **authenticate_kwargs)
        self.save_login_history(self.user)

        return True


class LoginSerializer(CustomTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        return super().validate(attrs)

    @transaction.atomic
    def login(self):
        refresh = self.get_token(self.user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": self.user.id,
                "fullname": self.user.fullname,
                "user_code": self.user.user_code,
                "last_name": self.user.last_name,
                "first_name": self.user.first_name,
                "is_superuser": self.user.is_superuser,
            },
        }
