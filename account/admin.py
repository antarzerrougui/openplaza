from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from .models import User


class UserCreationForm(UserCreationForm):
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
        }
    email = forms.EmailField(label=_("Email"),help_text="Required.")
    class Meta:
        model = get_user_model()
        fields = ("email","username",)

    def clean_username(self):
        UserModel = get_user_model()
        username = self.cleaned_data["username"]
        try:
            UserModel.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_email(self):
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        try:
            UserModel.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

class UserChangeForm(UserChangeForm):
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        }
    email = forms.EmailField(label=_("Email"),help_text="Required.")
    class Meta:
        model = get_user_model()

class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('email','username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username', 'password1', 'password2')}
        ),
    )

admin.site.register(User, UserAdmin)