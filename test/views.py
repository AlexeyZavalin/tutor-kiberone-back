from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView

from mainapp.mixins import StudentOrTutorRequiredMixin
from test.models import Test, TestResult
from test import services


class TestListView(StudentOrTutorRequiredMixin, ListView):
    """Список тестов"""
    template_name = 'test/test/list.html'
    model = Test
    context_object_name = 'tests'
    paginate_by = 15
    queryset = Test.objects.all()


class TestView(StudentOrTutorRequiredMixin, TemplateView):
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
        test_user = request.user if request.user.is_authenticated else \
            request.student if request.student else None
        data = request.POST
        test_result = services.create_test_result(test_user, test_id, data)
        if test_result:
            return HttpResponseRedirect(
                reverse_lazy('test:test-result',
                             kwargs={
                                 'pk': test_result.pk,
                                 'test_id': test_id
                             })
            )
        return HttpResponseRedirect(
            reverse_lazy(
                'test:test',
                 kwargs={
                     'test_id': test_id
                 }
            )
        )



class TestResultDetailView(StudentOrTutorRequiredMixin, DetailView):
    """Страница с результатом теста"""
    template_name = 'test/test_result/detail.html'
    model = TestResult
    context_object_name = 'test_result'


class TestResultListView(StudentOrTutorRequiredMixin, ListView):
    """Список резултатов теста"""
    login_url = reverse_lazy('authapp:login')
    template_name = 'test/test_result/list.html'
    model = TestResult
    context_object_name = 'test_results'
    paginate_by = 15

    def get_queryset(self, *args, **kwargs):
        queryset = TestResult.objects.filter(
            test__pk=self.kwargs.get('test_id')
        )
        if self.request.user:
            return queryset.filter(tutor=self.request.user)
        if self.request.student:
            return queryset.filter(student=self.request.student)
        return queryset


class TestResultsListView(ListView, StudentOrTutorRequiredMixin):
    template_name = 'test/test_result/test_list.html'
    model = Test
    context_object_name = 'tests'
    paginate_by = 15
    queryset = Test.objects.all()
