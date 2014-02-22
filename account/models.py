from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from directory.models import Country,CountryRegion

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


class Address(models.Model):
    customer = models.ForeignKey(User,blank=True,null=True)
    firstname = models.CharField("First name",max_length=254)
    lastname = models.CharField("Last name",max_length=254)
    middlename = models.CharField("Middle name",max_length=254)
    country = models.ForeignKey(Country,to_field = 'country_id')
    region = models.CharField("Region",max_length=254)
    region_id = models.ForeignKey(CountryRegion, blank=True,null=True)
    postcode = models.CharField("Postcode",max_length=254)
    city = models.CharField("City",max_length=254)
    street = models.CharField("Street",max_length=254)
    telephone = models.CharField("Telephone",max_length=64,blank=True,null=True)
    fax = models.CharField("Fax",max_length=64,blank=True,null=True)
    prefix = models.CharField("Prefix",max_length=64,blank=True,null=True)
    suffix = models.CharField("Suffix",max_length=64,blank=True,null=True)
    is_active = models.BooleanField("Is active",default=True)
    created_at = updated_at = models.DateTimeField(_('Created At'),auto_now_add= True,null=True)
    updated_at = models.DateTimeField(_('Updated At'),auto_now_add= True,null=True,blank=True)


