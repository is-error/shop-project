from django.contrib import admin
from users.models import User, LoginHistory

admin.site.register(User)
admin.site.register(LoginHistory)
