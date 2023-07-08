import random
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, fullname, email, password, **extra_fields):
        if not email:
            raise ValueError("Email đã tồn tại")
        email = self.normalize_email(email)
        user = self.model(
            fullname=fullname, email=email, is_active=True, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, fullname, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        user = self._create_user(fullname, email, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, fullname, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        user = self._create_user(fullname, email, password, **extra_fields)
        return user


class User(AbstractUser):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    user_code = models.CharField(
        max_length=10,
        blank=True,
        editable=False,
        unique=True,
    )

    # default columns
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    user_created = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="account_user_created",
        null=True,
        blank=True,
    )
    user_updated = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="account_user_updated",
        null=True,
        blank=True,
    )
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["fullname"]

    # remove default fields
    username = None
    is_staff = None
    last_login = None
    date_joined = None

    objects = UserManager()

    def __str__(self):
        return "({}) {} - {}".format(self.id, self.user_code, self.fullname)

    @property
    def is_staff(self):
        return self.is_superuser

    def create_user_code_ref_number(self):
        not_unique = True
        while not_unique:
            unique_ref = random.randint(1000000000, 9999999999)
            if not User.objects.filter(user_code=unique_ref):
                not_unique = False
        return str(unique_ref)

    def save(self, *args, **kwargs):
        fullname_arr = self.fullname.split(" ")
        self.first_name = fullname_arr.pop(-1)
        self.last_name = " ".join(fullname_arr)
        if not self.user_code:
            self.user_code = self.create_user_code_ref_number()
        super(User, self).save(*args, **kwargs)
