from django.db import models
from django.utils import timezone


class LoginHistory(models.Model):
    user = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="login_histories",
        null=True,
        blank=True,
    )
    ip_address = models.CharField(max_length=125)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    # default columns
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - {} - {}".format(self.user.fullname, self.ip_address, self.location)
