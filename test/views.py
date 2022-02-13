from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView

from test.models import Test, TestResult, UserAnswer, Answer


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test = Test.objects.get(pk=kwargs.get('test_id'))
        context['test'] = test
        context['questions'] = test.questions.all()
        return context

    def post(self, request, **kwargs):
        test_id = kwargs.get('test_id')
        data = request.POST
        test_result = TestResult()
        test_result.testees_name = data.get('name')
        test_result.test = Test.objects.get(id=test_id)
        test_result.save()
        answers = [UserAnswer(answer_id=value, test_result_id=test_result.pk)
                   for key, value in data.items()
                   if key.startswith('question')]
        UserAnswer.objects.bulk_create(answers)
        correct_counter = len(list(filter(lambda x: x.answer.is_correct,
                                          answers)))
        if correct_counter >= test_result.test.corrects_to_pass:
            test_result.passed = True
            test_result.correct_count = correct_counter
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
