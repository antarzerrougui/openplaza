from django.db.models import CharField,BooleanField
from django.contrib.sites.models import Site
from django.conf import settings



Site.add_to_class('code', CharField(max_length=64,unique=True))
Site.add_to_class('api', CharField(max_length=255))
Site.add_to_class('key', CharField(max_length=255))
Site.add_to_class('secret', CharField(max_length=255))
Site.add_to_class("type",CharField(max_length=64,choices = settings.WEBSITE_TYPE))
Site.add_to_class('is_active', BooleanField())