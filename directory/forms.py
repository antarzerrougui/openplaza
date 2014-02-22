from django.forms import ModelForm
from .models import Country,CountryRegion,CurrencyRate


class CountryModelForm(ModelForm):
    class meta:
        model = Country

class CountryRegionModelForm(ModelForm):
    class meta:
        model = CountryRegion


class CurrencyRateModelForm(ModelForm):
    class meta:
        model = CurrencyRate