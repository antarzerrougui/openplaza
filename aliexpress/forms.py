from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site

class AuthForm(forms.Form):
    account = forms.EmailField(required=True)
    password = forms.CharField(required=True,widget=forms.PasswordInput)

class TaobaoForm(forms.Form):
    links = forms.CharField(required=True,widget=forms.Textarea)
    site = forms.ModelChoiceField(queryset=Site.objects.filter(type='aliexpress').filter(is_active = True))
    account = forms.EmailField(required=True)


    def clean_links(self):
        links = self.cleaned_data['links']

        return links.split("\r\n")