from django.db import models


class UserType(models.TextChoices):
    USER = 'user'
    STAFF = 'staff'
    ADMIN = 'admin'