from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}),
                             label="E-mail")
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )


class RemoveGroupForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label=_('Пароль'))
    group_id = forms.CharField(widget=forms.HiddenInput)
