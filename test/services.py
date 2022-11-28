from django.http import QueryDict

from test.models import Test, TestResult, UserAnswer


def create_test_result(test_id: int, data: QueryDict) -> TestResult:
    """
    Создаем результаты теста
    """
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
    if test_result.test.corrects_to_pass and correct_counter >= \
            test_result.test.corrects_to_pass:
        test_result.passed = True
        test_result.correct_count = correct_counter
        test_result.save()
    return test_result
