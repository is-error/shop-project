from rest_framework import serializers

from users.models import LoginHistory


class LoginHistorySerializer(serializers.ModelSerializer):
    login_at = serializers.DateTimeField(source="created_at")
    coordinates = serializers.SerializerMethodField()

    class Meta:
        model = LoginHistory
        fields = ("ip_address", "login_at", "location", "coordinates")

    def get_coordinates(self, obj):
        return [obj.latitude, obj.longitude]
