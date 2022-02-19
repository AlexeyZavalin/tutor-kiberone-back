from django import forms

from test.models import Question, Answer


class QuestionForm(forms.ModelForm):
    """
    Форма с вопросом
    """
    answers = forms.ModelChoiceField(queryset=Answer.objects.none(),
                                     empty_label=None, label='')
    multiple_answers = forms.ModelMultipleChoiceField(
        queryset=Answer.objects.none(),
        label='')
    answer = forms.CharField(widget=forms.Textarea, label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        question = kwargs.get('instance')
        if question.type == Question.ONE_CORRECT:
            self.fields['answers'].widget = forms.RadioSelect()
            queryset = question.answers.all()
            self.fields['answers'].queryset = queryset
            self.desc = question.question_text
            del self.fields['answer']
            del self.fields['multiple_answers']
        elif question.type == Question.COUPLE_CORRECTS:
            self.fields['multiple_answers'].widget = forms.CheckboxSelectMultiple()
            queryset = question.answers.all()
            self.fields['multiple_answers'].queryset = queryset
            self.desc = question.question_text
            del self.fields['answer']
            del self.fields['answers']
        elif question.type == Question.TEXT:
            self.desc = question.question_text
            del self.fields['answers']
            del self.fields['multiple_answers']

    class Meta:
        model = Question
        fields = ('answers', 'answer')
