from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import logout, login
from django.views.generic import FormView
from django.contrib.auth.views import LoginView


from .forms import CreateProfileForm, PasswordResetForm, SignInForm, SignUpForm

def test(request):
    return HttpResponse('dasdas')

class MyFormView(FormView):
    http_method_names = ['get', 'post']
    success_url = reverse_lazy(viewname='blog_auth:main')

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        form.save()
        return redirect(to=self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        self.extra_context = dict(errors_forms=form.errors)
        return super().form_invalid(form=form)

class SignUpView(MyFormView):
    form_class = SignUpForm
    template_name = 'account/sign_up.html'

class CreateProfileView(MyFormView):
    form_class = CreateProfileForm
    template_name = 'account/create_profile.html'

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(user=self.request.user, **self.get_form_kwargs()) # add user

class SignInView(LoginView):
    form_class = SignInForm
    template_name = 'account/sign_in.html'
    success_url = reverse_lazy(viewname='blog_auth:main')
    unactive_url = reverse_lazy(viewname='blog_auth:create_profile')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

    def get_unactive_url(self):
        return self.unactive_url

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            login(self.request, form.get_user())
            return redirect(to=self.get_unactive_url())
        return super().form_valid(form)

class ResetPasswordView(MyFormView):
    form_class = PasswordResetForm
    template_name = 'account/reset_password.html'