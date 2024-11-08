from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from allauth.account.models import EmailAddress
from profiles.models import ClientProfile, UserProfile
from .managers import UserManager


class User(AbstractUser):
    class Types(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CLIENT = "CLIENT", "Client"
        USER = "USER", "User"

    type = models.CharField(
        'Tipo de Usuário',
        max_length=20,
        choices=Types.choices,
        default=Types.USER
    )
    username = None
    email = models.EmailField(_('email address'), unique=True)
    # first_name = None
    # last_name = None
    # should move to CommonProfile.full_name ?

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    @classmethod
    def get_developer_user(cls):
        return cls.objects.filter(email=settings.ADMIN_EMAIL).first()

    @classmethod
    def force_verify_email(cls, user):
        email = EmailAddress.objects.filter(email=user.email).first()
        if not email:
            email = EmailAddress.objects.create(
                user_id=user.id, email=user.email,
            )
        email.verified = True
        email.primary = True
        email.save()

    @property
    def is_admin(self):
        return self.type == self.Types.ADMIN

    @property
    def is_client(self):
        return self.type == self.Types.CLIENT

    @property
    def is_user(self):
        return self.type == self.Types.USER

    @property
    def client_profile(self):
        return ClientProfile.objects.first()

    @property
    def profile(self):
        if self.is_user:
            return UserProfile.objects.filter(user=self).first()
        return self.client_profile

    def get_notifications(self):
        from document.views.notification import get_tasks
        return get_tasks(self.id)
