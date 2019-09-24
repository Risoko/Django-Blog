from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView 

from blog_auth.views import MyFormView
from .forms import ChangeEmailForm, ChangePasswordForm

@method_decorator(
    decorator=login_required(login_url=reverse_lazy('blog_auth:login')),
    name='dispatch'
    )
class ChangePasswordView(MyFormView):
    template_name = 'user_operation/change_password.html'
    form_class = ChangePasswordForm

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(user=self.request.user, **self.get_form_kwargs())
    
class ChangeEmailView(ChangePasswordView):
    template_name = 'user_operation/change_email.html'
    form_class = ChangeEmailForm

