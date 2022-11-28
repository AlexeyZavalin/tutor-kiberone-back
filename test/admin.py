from django.contrib import admin
from django import forms

from ckeditor.widgets import CKEditorWidget

from test.models import Answer, Question, Test, TestResult, UserAnswer


class QuestionAdminForm(forms.ModelForm):
    question_text = forms.CharField(widget=CKEditorWidget(), label='Текст '
                                                                   'вопроса')

    class Meta:
        model = Question
        fields = '__all__'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_filter = ('tests',)

    class AnswerInline(admin.TabularInline):
        model = Answer
        extra = 1
        fields = ['answer_text', 'is_correct']

    inlines = [AnswerInline]


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    filter_horizontal = ('questions',)


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):

    class UserAnswerInline(admin.StackedInline):
        model = UserAnswer
        extra = 0
        can_delete = False
        can_add = False
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        readonly_fields = ['answer']

    list_display = ['testees_name', 'test', 'date', 'passed']
    date_hierarchy = 'date'
    search_fields = ['testees_name', 'test__name']
    list_filter = ['test__name']
    readonly_fields = ['test', 'passed']
    inlines = [UserAnswerInline]
