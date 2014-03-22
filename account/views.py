from django.views.generic import TemplateView,CreateView
from django.contrib.auth import login as auth_login,authenticate
from django.core.urlresolvers import reverse_lazy
from .forms import *

class Profile(TemplateView):

    template_name = "registration/login.html"

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class Register(CreateView):
    template_name = "registration/register.html"

    success_url = reverse_lazy('profile')

    form_class = RegisterForm

    def form_valid(self, form):
        form.save()
        user = authenticate(email=form.cleaned_data.get('email'), password=form.cleaned_data.get('confirm_password'))
        if user is not None:
            auth_login(self.request, user)
        return super(Register, self).form_valid(form)