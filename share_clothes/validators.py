from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def check_password(password):
    test_string = '[@_!#$%^&*()<>?/\|}{~:]'
    if len(password) < 8:
        raise ValidationError(_('Hasło powinno zawierać conajmniej 8 znaków'), code='invalid')
    elif not any(x.isupper() for x in password):
        raise ValidationError(_('Hasło powinno zawierać conajmniej i dużą literę'), code='invalid')
    elif not any(x.isdigit() for x in password):
        raise ValidationError(_('Hasło powinno zawierać conajmniej i cyfre'), code='invalid')
    elif not any(ele in test_string for ele in password):
        raise ValidationError(_('Hasło powinno zawierać conajmniej 1 znak specjalny'), code='invalid')









