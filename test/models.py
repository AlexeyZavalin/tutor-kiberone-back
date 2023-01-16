from django.db import models


class Question(models.Model):
    """Вопрос"""
    QUESTION_TYPES = (
        (1, 'Один правильный ответ'),
        (2, 'Несколько правильных ответов'),
        (3, 'Развернутый ответ')
    )
    question_text = models.TextField(
        max_length=500,
        null=False,
        blank=False,
        verbose_name='Текст вопроса'
    )
    type = models.PositiveSmallIntegerField(
        choices=QUESTION_TYPES,
        verbose_name='Тип вопроса',
        default=QUESTION_TYPES[0]
    )

    def __str__(self):
        return self.question_text[:30]

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    """Ответ"""
    question = models.ForeignKey(
        to=Question,
        on_delete=models.SET_NULL,
        verbose_name='Вопрос',
        null=True,
        related_name='answers'
    )
    answer_text = models.TextField(
        null=True,
        blank=True,
        max_length=500,
        verbose_name='Текст ответа'
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name='Является верным ответом'
    )

    def __str__(self):
        return self.answer_text[:50]

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Test(models.Model):
    """Тест"""
    name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Название теста'
    )
    questions = models.ManyToManyField(
        to=Question,
        verbose_name='Вопросы',
        related_name='tests',
        blank=True
    )
    corrects_to_pass = models.PositiveSmallIntegerField(
        verbose_name='Количество правильных ответов для прохождения',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class TestResult(models.Model):
    """Результат теста"""
    testees_name = models.CharField(
        max_length=70,
        null=False,
        blank=False,
        verbose_name='Имя тестируемого'
    )
    student = models.ForeignKey(
        to='mainapp.Student',
        null=True,
        verbose_name='Ученик',
        on_delete=models.CASCADE
    )
    tutor = models.ForeignKey(
        to='authapp.Tutor',
        null=True,
        verbose_name='Тьютор',
        on_delete=models.CASCADE
    )
    test = models.ForeignKey(
        to=Test,
        on_delete=models.CASCADE,
        verbose_name='Тест'
    )
    correct_count = models.PositiveSmallIntegerField(
        default=0,
        null=True,
        blank=False,
        verbose_name='Количество верных ответов'
    )
    passed = models.BooleanField(
        default=False,
        verbose_name='Тест пройден'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата прохождения'
    )

    def __str__(self):
        return self.testees_name

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'


class UserAnswer(models.Model):
    """Ответ пользователя"""
    answer = models.ForeignKey(
        to=Answer,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Ответ пользователя'
    )
    test_result = models.ForeignKey(
        to=TestResult,
        on_delete=models.CASCADE,
        verbose_name='Тест',
        null=True
    )

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'

    def __str__(self):
        return f'{self.answer.answer_text} - ' \
               f'{"верно" if self.answer.is_correct else "не верно"}'
