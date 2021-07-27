from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from mainapp.models import Tutor


class LoginForm(AuthenticationForm):

    def clean(self):
        user = authenticate(username=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))
        if user is None:
            raise forms.ValidationError('Введён некорректный e-mail или пароль, попробуйте ввести их ещё раз!',
                                        code='invalid_login_password')
        if not user.is_active:
            raise forms.ValidationError('Вам закрыт доступ к сайту!', code='access_denied')
