import hashlib

from datetime import date

from django.db import models, IntegrityError
from django.urls import reverse
from django.utils import timezone
from django.db.models import F
from solo.models import SingletonModel

from mainapp.mixins import DeletedMixin


SYMBOLS_FOR_SLUG = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'e',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'c',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sh',
    'ъ': '',
    'ы': 'y',
    'ь': '',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
    ' ': '_',
}


class ActiveGroupsManager(models.Manager):
    def get_queryset(self):
        return Group.objects.filter(is_deleted=False)


class ActiveStudentsManager(models.Manager):
    def get_queryset(self):
        return Student.objects.filter(is_deleted=False)


class Location(DeletedMixin):
    """
    Локация
    """
    address = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='Адрес локации'
    )
    short_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Краткое наименование'
    )

    class Meta:
        verbose_name_plural = 'Локации'
        verbose_name = 'Локация'

    def __str__(self):
        return self.short_name


class AvailableTime(DeletedMixin):
    """
    Доступное время для урока
    """
    time_start = models.TimeField(verbose_name='Время начала урока')
    time_end = models.TimeField(verbose_name='Время завершения урока')

    class Meta:
        verbose_name = 'Доступное время'
        verbose_name_plural = 'Доступное время'
        unique_together = ('time_start', 'time_end')

    def __str__(self):
        return f'{self.time_start.strftime("%H:%M")}-' \
               f'{self.time_end.strftime("%H:%M")}'


class Group(DeletedMixin):
    """
    Модель для хранения информации о группе
    """
    objects = models.Manager()
    active = ActiveGroupsManager()

    DAYS_OF_WEEK_CHOICES = (
        ('mn', 'Понедельник'),
        ('tu', 'Вторник'),
        ('we', 'Среда'),
        ('th', 'Четверг'),
        ('fr', 'Пятница'),
        ('st', 'Суббота'),
        ('sn', 'Воскресенье'),
    )
    available_time = models.ForeignKey(
        AvailableTime,
        verbose_name='Время',
        on_delete=models.SET_NULL,
        null=True
    )
    available_location = models.ForeignKey(
        Location,
        verbose_name='Локация',
        on_delete=models.SET_NULL,
        null=True
    )
    day_of_week = models.CharField(max_length=2, choices=DAYS_OF_WEEK_CHOICES,
                                   default=DAYS_OF_WEEK_CHOICES[0],
                                   verbose_name='День недели')
    tutor = models.ForeignKey('authapp.Tutor', on_delete=models.SET_DEFAULT,
                              default=None, null=True, verbose_name='Тьютор',
                              related_name='tutor')
    temporary_tutor = models.ForeignKey('authapp.Tutor',
                                        on_delete=models.SET_NULL,
                                        default=None, null=True,
                                        verbose_name='Временный тьютор',
                                        related_name='temp_tutor', blank=True)
    slug = models.SlugField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        unique_together = ('available_time', 'available_location',
                           'day_of_week')
        db_table = 'group'
        
    def save(self, *args, **kwargs):
        self.slug = self.slugify()
        super(Group, self).save(*args, *kwargs)
        

    def __str__(self):
        return f'{self.get_day_of_week_display()} ' \
               f'{self.available_location} {self.available_time}'

    def slugify(self):
        return ''.join([SYMBOLS_FOR_SLUG.get(symbol, symbol) for symbol in
                        list(f'{self.pk}{self.available_location.address.lower()}'[:8])])

    @property
    def students_amount(self):
        return self.students.filter(is_deleted=False).count()


class Student(DeletedMixin):
    """
    Модель для хранения информации об ученике
    """
    objects = models.Manager()
    active = ActiveStudentsManager()

    name = models.CharField(max_length=50, blank=False,
                            verbose_name='Фамилия Имя')
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              verbose_name='Группа',
                              related_name='students')
    kiberon_amount = models.PositiveIntegerField(default=0,
                                                 verbose_name='Количество '
                                                              'киберонов')
    info = models.TextField(max_length=250, blank=True,
                            verbose_name='Информация')
    visited_date = models.DateField(
        default=None,
        verbose_name='Последняя дата посещения',
        null=True,
        blank=True)
    gmail_name = models.EmailField(default=None, verbose_name='Gmail',
                                   null=True, blank=True, max_length=70)
    # выводить только в админке
    gmail_password = models.CharField(
        default=None,
        null=True,
        blank=True,
        max_length=30,
        verbose_name='Gmail password (выводить только в админке)'
    )
    token = models.CharField(max_length=64, null=True, unique=True)
    code = models.CharField(max_length=8, null=True, blank=True)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        db_table = 'student'

    def __str__(self):
        return self.name

    def create_token(self):
        """создаем токен из фамилии и имени по sha256"""
        self.token = hashlib.sha256(f'{self.name}{self.pk}'.encode(
            'utf8')).hexdigest()
        self.code = self.token[:8]
        self.save()

    def add_kiberons(self, amount):
        self.kiberon_amount = F('kiberon_amount') + amount
        self.save()

    def delete_kiberons(self, amount):
        self.kiberon_amount = F('kiberon_amount') - amount
        self.save()

    def get_absolute_url(self):
        return reverse('mainapp:student-list',
                       kwargs={'group_id': self.group.pk})

    @property
    def visited_at_current_date(self) -> bool:
        """ посетил в текущую дату """
        return date.today() == self.visited_date


class Kiberon(models.Model):
    """
    Модель для хранения значению киберона по достижениям
    """
    VISIT = 'visit'
    EYES = 'eyes'
    FASTEST = 'fastest'
    HOMEWORK = 'homework'
    INSTAGRAM = 'instagram'
    SOCIAL = 'social'
    ANSWER = 'answer'
    CUSTOM = 'custom'
    PERFECT_BEHAVIOUR_IN_MODULE = 'behavior'
    HELP_TO_FRIEND = 'help'
    HELP_TO_ASSISTENT = 'assist'
    USEFUL_RULE = 'rule'
    ACHIEVEMENT_CHOICES = (
        (VISIT, 'Посещение урока'),
        (EYES, 'Разминка глаз'),
        (FASTEST, 'Быстрее всех завершил задание'),
        (HOMEWORK, 'За выполнение домашнего задания'),
        (INSTAGRAM, 'За пост в instagram'),
        (SOCIAL, 'За посты в соц. сети'),
        (ANSWER, 'За ответ в конце урока'),
        (CUSTOM, 'Свое достижение'),
        (PERFECT_BEHAVIOUR_IN_MODULE,
         'Прошел модуль без замечаний по поведению'),
        (HELP_TO_FRIEND, 'Помог другу'),
        (HELP_TO_ASSISTENT, 'Помог ассистенту с уборкой'),
        (USEFUL_RULE, 'Придумал полезное правило для школы')
    )
    achievement = models.CharField(max_length=10, choices=ACHIEVEMENT_CHOICES,
                                   default=ACHIEVEMENT_CHOICES[0],
                                   unique=True, verbose_name='Достижение')
    value = models.PositiveSmallIntegerField(default=5, blank=False,
                                             verbose_name='Количество '
                                                          'киберонов')

    class Meta:
        verbose_name = 'Печать'
        verbose_name_plural = 'Печати'
        db_table = 'kiberon'

    def __str__(self):
        return f'{self.get_achievement_display()} - {self.value}к'


class KiberonStudentReg(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                verbose_name='Студент')
    kiberon = models.ForeignKey(Kiberon, on_delete=models.CASCADE,
                                verbose_name='Достижение')
    date = models.DateTimeField(verbose_name='Дата', default=timezone.now)
    tutor = models.ForeignKey('authapp.Tutor', on_delete=models.CASCADE,
                              verbose_name='Тьютор')
    custom_kiberons = models.PositiveSmallIntegerField(
        verbose_name='Свое количество киберонов', default=0)
    custom_achievement = models.CharField(max_length=100, default='',
                                          blank=True,
                                          verbose_name='Кастомное достижение')

    class Meta:
        verbose_name = 'Запись о печати'
        verbose_name_plural = 'Записи о печатях'
        ordering = ('-date',)
        db_table = 'kiberon_register'

    def __str__(self):
        return f'{self.student.name} - ' \
               f'{self.kiberon.get_achievement_display()} - {self.date}'

    def save(self, **kwargs):
        if self.kiberon.achievement == Kiberon.CUSTOM:
            self.student.add_kiberons(self.custom_kiberons)
        else:
            # ставим последнюю дату посещения для студента
            if self.kiberon.achievement == Kiberon.VISIT:
                self.student.visited_date = date.today()
                self.student.save()

            reg = KiberonStudentReg.objects.filter(student=self.student,
                                                   kiberon=self.kiberon,
                                                   date=self.date)
            if reg.count() == 0:
                self.student.add_kiberons(self.kiberon.value)
            else:
                raise IntegrityError
        super().save(**kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.kiberon.achievement == 'custom':
            self.student.delete_kiberons(self.custom_kiberons)
        else:
            self.student.delete_kiberons(self.kiberon.value)
        super().delete()


class SiteConfiguration(SingletonModel):
    """настройки сайта"""
    fair_is_active = models.BooleanField(
        default=False,
        verbose_name='Ярмарка запущена'
    )

    def __str__(self):
        return 'Настройки сайта'

    class Meta:
        verbose_name = 'Настройки сайта'
