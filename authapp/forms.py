from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
    """Форма входа на сайт"""
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}),
                             label="E-mail")
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )


class TutorPasswordChangeForm(PasswordChangeForm):
    pass


class TutorPasswordResetForm(PasswordResetForm):
    pass
