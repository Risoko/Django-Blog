from datetime import datetime
from random import randint, sample
from string import ascii_lowercase

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import BlogProfile, User
from .email_tool import send_email

class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'nick', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

    def clean_nick(self):
        nick = self.cleaned_data['nick']
        if nick.isdigit():
            raise forms.ValidationError(
                message=_("Nick can't be only digit.")
            )
        return nick

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.isdigit():
            raise forms.ValidationError(
                message=_("Username can't be only digit.")
            )
        return username

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        nick = self.cleaned_data.get('nick')
        if username == nick:
            raise forms.ValidationError(
                message=_("Nick and username can't be same %(username)s != %(nick)s"),
                params={
                        'username': username,
                        'nick': nick
                }
            )
        return self.cleaned_data
        
    def save(self, commit=True):
        """
        Method create user in database.
        """
        user = super().save(commit=False)
        password = self.cleaned_data['password1']
        user.set_password(password)
        message = f'''
        You have successfully created an account.
        To activate them you must first log in.
        Your login details:
            username: {user.username}
            password: {password}
        '''
        if commit:
            user.send_email_user(
                subject='Registation',
                message=message
            )
            user.save()
        return user

class CreateProfileForm(forms.ModelForm):
    birth_year_choices = (str(year) for year in range(1930, datetime.now().year - 3 ))
    date_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=list(birth_year_choices))
    )
    class Meta:
        model = BlogProfile
        exclude = ['date_birth', 'number_article']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_first_name(self):
        """
        Method return first name in correct format.
        Example:
          User enter: jOhn
          Method return: John
        """
        return self.cleaned_data['first_name'].capitalize()

    def clean_last_name(self):
        """
        Method return last name in correct format.
        Example
          User enter: koWalski
          Method return: Kowalski
        """
        return self.cleaned_data['last_name'].capitalize()

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.date_birth = self.cleaned_data.get('date_birth')
        if commit:
            profile.save()
            self.user.user_profile = profile
            self.user.is_active = True
            self.user.save()
            return
        return profile

class SignInForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'is_ban': _(
            "User about this username: %(username)s is banned."
            " Unlocking your account will: %(end_ban)s"
        )
    }

    def confirm_login_allowed(self, user):
        """
        If user is ban, method raise exception"""
        user.unblocking_user()
        if user.is_ban:
            raise forms.ValidationError(
                message=self.error_messages['is_ban'],
                code='is_ban',
                params={
                    'username': user.username,
                    'end_ban': user.end_ban
                }
            )

class PasswordResetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def _get_new_password(self, password_lenght=8):
        """
        The method returns a new random user password.
        """
        return ''.join(sample(ascii_lowercase, password_lenght))

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.isdigit():
            raise forms.ValidationError(
                message=_("Username can't be only digit.")
            )
        return username

    def clean(self):
        """
        The method check if the email matches the username.
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username, email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                message=_('The user with the given e-mail address or name does not exist.')
            )
        return self.cleaned_data

    def save(self):
        """
        The method sets a new user password and 
        sends a message to the provided email address with a new password.
        """
        email = self.cleaned_data['email']
        user = User.objects.get(email=email)
        new_password = self._get_new_password()
        message = f'''
        Hi {self.cleaned_data['username']}.
        You are reset your password.
        Your new password: {new_password}
        '''
        user.set_password(new_password)
        user.save()
        user.send_email_user(
            subject='Reset Password',
            message=message
        )
        return new_password










        
        
    