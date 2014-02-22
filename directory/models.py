from django.db import models

class Country(models.Model):
    country_id = models.CharField("Country code",primary_key=True,max_length=32)
    iso2_code = models.CharField("Country ISO2 code",max_length=32)
    iso3_code = models.CharField("Country ISO3 code",max_length=32)


class CountryRegion(models.Model):
    country = models.ForeignKey(Country,related_name="region_country_id")
    code = models.CharField("Code",max_length=32)
    name = models.CharField("Default name",max_length=254)

class CurrencyRate(models.Model):
    currency_from = models.CharField("Currency from",max_length=32)
    currency_to = models.CharField("Currency to",max_length=32)
    rate = models.DecimalField("Rate",max_digits=10,decimal_places=2)
