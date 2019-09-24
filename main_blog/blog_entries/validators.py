from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def check_is_digit_validator(value_field):
    if value_field.isdigit():
        raise ValidationError(
            message=_("You can't use only digit.")
        )