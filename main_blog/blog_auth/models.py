from datetime import date
from functools import partial
from pycountry import countries

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils.timezone import timedelta, now as date_now
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from .email_tool import send_email
from .mangers import BlogProfileManager

class BlogProfile(models.Model):
    MALE_SEX = 'M'
    FEMALE_SEX = 'F'
    SEX_CHOICES = [
        (MALE_SEX, 'Male'),
        (FEMALE_SEX, 'Female')
    ]
    COUNTRY_CHOICES = list((country.alpha_2, country.name) for country in countries)
    first_name_validator = RegexValidator(
        regex=r'^[a-zA-Z]*$',
        message=_('First name must contain only letters.')
    )
    last_name_validator = RegexValidator(
        regex=r'^[a-zA-Z]*$',
        message=_('Last name must contain only letters.'),
    )
    sex = models.CharField(
        verbose_name=_('sex'),
        max_length=20,
        choices=SEX_CHOICES,
        default=MALE_SEX
    )
    first_name = models.CharField(
        verbose_name=_('name'),
        max_length=30,
        validators=[first_name_validator, MinLengthValidator(3)],
        help_text=_('Enter your name.')
    )
    last_name = models.CharField(
        verbose_name=_('last name'),
        max_length=30,
        validators=[last_name_validator, MinLengthValidator(3)],
        help_text=_('Enter your country.')
    )
    country = models.CharField(
        verbose_name='country',
        max_length=200,
        help_text=_('Enter your country.'),
        choices=COUNTRY_CHOICES,
        default=COUNTRY_CHOICES[79]   
    )
    date_birth = models.DateField(
        verbose_name=_('date of birth'),
        help_text=_('Date of your birth.'),
    )
    number_article = models.SmallIntegerField(
        verbose_name=_('Number of articles written by the user'),
        default=0
    )
    objects = BlogProfileManager()

    class Meta:
        verbose_name = _('blogprofile')
        verbose_name_plural = _('blogprofiles')

class User(AbstractUser):
    user_profile = models.ForeignKey(
        to=BlogProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    nick_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9]*$',
        message=_('Nick must be only alphanumeric.'),
        code='invalid_nick'
    )
    nick = models.CharField(
        verbose_name=_('nick'),
        max_length=20,
        unique=True,
        help_text=_('Enter nick name.'),
        validators=[nick_validator, MinLengthValidator(limit_value=4)],
        error_messages={
            'unique': _("A user with that nick already exists.")
        }
    )
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=100,
        unique=True,
        help_text=_('Enter email address.'),
        error_messages={
            'unique': _("A user with that email already exists.") 
        }
    )
    is_ban = models.BooleanField(
        verbose_name=_('ban'),
        default=False,
        help_text=_(
            'If the user is banned he has no access to the account.'
            'The account lock ends when the ban date expires.'
        )
    )
    end_ban = models.DateTimeField(
        verbose_name=_('end date of the ban'),
        blank=True,
        null=True,
        help_text=_('When the ban ends, the account is unbanned.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        )
    )
    first_name = None
    last_name = None

    class Meta(AbstractUser.Meta):
            swappable = 'AUTH_USER_MODEL'

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.user_profile.first_name, user.user_profile.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user.""" 
        return self.user_profile.first_name

    def unblocking_user(self):
        """
        If the lock time has expired, the method unblocks the user.
        """
        if self.end_ban is None:
            return      
        if self.end_ban < date_now():
            self.is_ban = False
            self.end_ban = None
            self.save()
            self.send_email_user(
                subject='Unban',
                message=f'Your account has been unbanned.'
            )
        return

    def ban_user(self, minutes=0, hours=0, days=0, weeks=0):
        """
        Method ban user. You can block a user for a certain amount:
          - minutes
          - hours
          - days
          - weeks
        """
        if self.is_superuser:
            raise ValidationError(
                message=_("You can't ban superuser.")
            )
        self.is_ban = True
        self.end_ban = date_now() + timedelta(
            minutes=minutes,
            hours=hours,
            days=days,
            weeks=weeks
        )
        self.save()
        self.send_email_user(
            subject='Ban account',
            message=f'Your account has been banned until {self.end_ban}.',
        )
        return

    def send_email_user(self, subject:str, message:str, from_email:str=None, additional_email:list=[]):
        """Send an email to this user."""
        from main_blog.settings import FROM_MAIL
        if from_email is None:
            from_email = FROM_MAIL
        all_emails = [self.email] + additional_email
        send_email(
            mail_from=from_email,
            mail_to=all_emails,
            mail_subject=subject,
            message=message
        )
        return

    def check_is_adult(self):
        date_birth = self.user_profile.date_birth
        adult_age = date(
            year=date_birth.year + 18,
            month=date_birth.month,
            day=date_birth.day
        )
        _date_now = date(
            year=date_now().year,
            month=date_now().month,
            day=date_now().day
        )
        return adult_age <= _date_now
        
        
