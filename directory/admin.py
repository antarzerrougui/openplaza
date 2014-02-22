from django.contrib import admin
from .models import Country,CountryRegion,CurrencyRate
from .forms import CountryModelForm,CountryRegionModelForm,CurrencyRateModelForm

class CountryAdmin(admin.ModelAdmin):
    form = CountryModelForm

class CountryRegionAdmin(admin.ModelAdmin):
    form = CountryRegionModelForm

class CurrencyRateAdmin(admin.ModelAdmin):
    form = CurrencyRateModelForm

admin.site.register(Country, CountryAdmin)
admin.site.register(CountryRegion, CountryRegionAdmin)
admin.site.register(CurrencyRate, CurrencyRateAdmin)
