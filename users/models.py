from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    is_teacher = models.BooleanField(
        _("Teacher status"),
        default=False,
        help_text=_("Indicates whether the user is a teacher."),
    )
