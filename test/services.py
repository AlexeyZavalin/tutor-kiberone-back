from typing import Union, Any

from django.db import transaction
from django.http import QueryDict

from authapp.models import Tutor
from mainapp.models import Student
from test.models import Test, TestResult, UserAnswer


def create_test_result(test_user: Union[Student, Tutor], test_id: int,
                       data: QueryDict) -> TestResult:
    """
    Создаем результаты теста
    """
    with transaction.atomic():
        test_result = TestResult()
        test_result.testees_name = f'{test_user.first_name} ' \
                                   f'{test_user.last_name}' \
            if isinstance(test_user, Tutor) else test_user.name \
            if isinstance(test_user, Student) else None
        test_result.test = Test.objects.get(id=test_id)
        test_result.save()
        answers = [UserAnswer(answer_id=value, test_result_id=test_result.pk)
                   for key, value in data.items()
                   if key.startswith('question')]
        UserAnswer.objects.bulk_create(answers)
        correct_counter = len(list(filter(lambda x: x.answer.is_correct,
                                          answers)))
        if test_result.test.corrects_to_pass and correct_counter >= \
                test_result.test.corrects_to_pass:
            test_result.passed = True
            test_result.correct_count = correct_counter
            test_result.save()
        return test_result
