from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class User(AbstractUser):
    AbstractUser._meta.get_field_by_name('email')[0]._unique = True

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    class Meta:
        db_table = "user"
        verbose_name = _('User')
        verbose_name_plural = _('User')

    def __unicode__(self):
        return self.email


class UserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')

        email = UserManager.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user
