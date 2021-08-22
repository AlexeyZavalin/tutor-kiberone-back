from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _

from .models import Group


class LoginForm(AuthenticationForm):
    """Форма входа на сайт"""
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}),
                             label="E-mail")
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )


class RemoveGroupForm(forms.Form):
    """Форма для удаления группы"""
    password = forms.CharField(widget=forms.PasswordInput, label=_('Пароль'))
    group_id = forms.CharField(widget=forms.HiddenInput)


class CreateGroupForm(forms.ModelForm):
    """Форма для создания группы"""
    class Meta:
        model = Group
        fields = ['time', 'location', 'day_of_week']
