from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView

from test.forms import QuestionForm
from test.models import Test, TestResult, UserAnswer, Question


class TestListView(ListView):
    """Список тестов"""
    template_name = 'test/test/list.html'
    model = Test
    context_object_name = 'tests'
    paginate_by = 15
    queryset = Test.objects.all()


class TestView(TemplateView):
    """Страница с тестом"""
    template_name = 'test/test/form.html'
    formset = modelformset_factory(Question, form=QuestionForm, extra=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test = Test.objects.get(pk=kwargs.get('test_id'))
        context['test'] = test

        context['formset'] = self.formset(queryset=test.questions.all())
        return context

    def post(self, request, **kwargs):
        test_id = kwargs.get('test_id')
        data = request.POST
        formset = self.formset(data)
        if formset.is_valid():
            test_result = TestResult()
            test_result.testees_name = data.get('name')
            test_result.test = Test.objects.get(id=test_id)
            test_result.save()

            answers = []
            correct_counter = 0
            for form in formset:
                data = form.cleaned_data
                question_type = data.get('id').type
                if question_type == Question.ONE_CORRECT:
                    user_answer = data.get('answers')
                    answers.append(UserAnswer(answer=user_answer,
                                              test_result_id=test_result.pk))
                    if user_answer.is_correct:
                        correct_counter += 1
                elif question_type == Question.COUPLE_CORRECTS:
                    user_answers = data.get('multiple_answers')
                    for user_answer in user_answers:
                        answers.append(
                            UserAnswer(answer=user_answer,
                                       test_result_id=test_result.pk)
                        )
                    if user_answers.count() == user_answers.filter(
                            is_correct=True).count():
                        correct_counter += 1
                elif question_type == Question.TEXT:
                    user_answer = data.get('answer')
                    answers.append(UserAnswer(answer_text=user_answer,
                                              test_result_id=test_result.pk))

            UserAnswer.objects.bulk_create(answers)
            test_result.correct_count = correct_counter
            if test_result.test.test_type == Test.REQUIRED and \
                    correct_counter >= test_result.test.corrects_to_pass:
                test_result.passed = True
            test_result.save()
            return HttpResponseRedirect(
                reverse_lazy('test:test-result', kwargs={'pk': test_result.pk})
            )


class TestResultDetailView(DetailView):
    """Страница с результатом теста"""
    template_name = 'test/test_result/detail.html'
    model = TestResult
    context_object_name = 'test_result'


class TestResultListView(ListView):
    """Список резултатов теста"""
    template_name = 'test/test_result/list.html'
    model = TestResult
    context_object_name = 'test_results'
    paginate_by = 15
    queryset = TestResult.objects.all()
