from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label= _('email'), help_text= _('Required.'))
    username = forms.RegexField(label= _('Username'),
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text = _('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages = {
            'invalid':_('This value may contain only letters, numbers and @/./+/-/_ characters.')
        }
    )
    password = forms.CharField(label= _('Password'), widget=forms.PasswordInput)
    confirm_password = forms.CharField(label= _('Password confirmation'),
        widget=forms.PasswordInput,
        help_text = _('Enter the same password as above, for verification.')
    )

    class Meta:
        fields = ['username', 'email','password','confirm_password']
        model = get_user_model()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            self._meta.model.objects.get(email=email)
        except self._meta.model.DoesNotExist:
            return email
        raise forms.ValidationError(_('A user with that email already exists.'))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            self._meta.model.objects.get(username=username)
        except self._meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(_('A user with that username already exists.'))

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get("password", "")
        password2 = self.cleaned_data.get("confirm_password")
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get("confirm_password"))
        if commit:
            user.save()
        return user