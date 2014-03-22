from django import forms
from django.utils.translation import ugettext_lazy as _



class AuthForm(forms.Form):
    account = forms.EmailField(required=True)
    password = forms.CharField(required=True,widget=forms.PasswordInput)
