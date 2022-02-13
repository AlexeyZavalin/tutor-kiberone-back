from django import forms

from test.models import Question


class QuestionForm(forms.Form):
    """
    Форма вопроса
    """
    answers = forms.ChoiceField(choices=[1, 2, 3])
