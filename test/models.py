from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from ckeditor.fields import RichTextField


class Question(models.Model):
    """Вопрос"""
    ONE_CORRECT = 1
    COUPLE_CORRECTS = 2
    TEXT = 3
    QUESTION_TYPES = (
        (ONE_CORRECT, 'Один правильный ответ'),
        (COUPLE_CORRECTS, 'Несколько правильных ответов'),
        (TEXT, 'Развернутый ответ')
    )
    question_text = RichTextField(
        max_length=500,
        null=False,
        blank=False,
        verbose_name='Текст вопроса',
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
    REQUIRED = 'required'
    OPTIONAL = 'optional'
    TEST_TYPES_CHOICES = [
        (REQUIRED, 'Обязательный'),
        (OPTIONAL, 'Не обязательный')
    ]
    name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Название теста'
    )
    test_type = models.CharField(
        choices=TEST_TYPES_CHOICES,
        max_length=8,
        null=True,
        default=REQUIRED,
        verbose_name='Тип теста'
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
    available_for_retest = models.BooleanField(
        default=True,
        verbose_name='Возможность перепрохождения теста'
    )
    days_for_retest = models.PositiveSmallIntegerField(
        verbose_name='Количество дней для возможности перепрохождения (1-7)',
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        null=False,
        blank=False
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
    answer_text = models.TextField(
        null=True,
        blank=False,
        verbose_name='Развернутый ответ'
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
               f'{"верно" if self.answer.is_correct else "не верно"}' if \
            self.answer else str(self.answer_text)
