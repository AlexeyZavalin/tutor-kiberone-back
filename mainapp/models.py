from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models import F
from django.core.exceptions import ValidationError

from mainapp.mixins import DeletedMixin


class ActiveGroupsManager(models.Manager):
    def get_queryset(self):
        return Group.objects.filter(is_deleted=False)


class ActiveStudentsManager(models.Manager):
    def get_queryset(self):
        return Student.objects.filter(is_deleted=False)


class Tutor(AbstractUser):
    full_name = models.CharField(blank=False, max_length=80,
                                 verbose_name='Фамилия Имя тьютора')
    email = models.EmailField(blank=False, max_length=50, verbose_name='Email тьютора',
                              unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Тьютор'
        verbose_name_plural = 'Тьюторы'

    def __str__(self):
        return self.full_name


class Group(DeletedMixin):
    """
    Модель для хранения информации о группе
    """
    objects = models.Manager()
    active = ActiveGroupsManager()

    TIMES_CHOICES = (
        ('1', '11:00'),
        ('2', '13:30'),
        ('3', '16:00'),
        ('4', '18:30'),
    )
    LOCATION_CHOICES = (
        ('1', 'КЮЧ1'),
        ('2', 'КЮЧ2'),
        ('3', 'Дзержинского'),
        ('4', 'Шеронова'),
    )
    DAYS_OF_WEEK_CHOICES = (
        ('mn', 'Понедельник'),
        ('tu', 'Вторник'),
        ('we', 'Среда'),
        ('th', 'Четверг'),
        ('fr', 'Пятница'),
        ('st', 'Суббота'),
        ('sn', 'Воскресенье'),
    )

    time = models.CharField(max_length=1, choices=TIMES_CHOICES, default=TIMES_CHOICES[0], verbose_name='Время')
    location = models.CharField(max_length=1, choices=LOCATION_CHOICES, default=LOCATION_CHOICES[0],
                                verbose_name='Локация')
    day_of_week = models.CharField(max_length=2, choices=DAYS_OF_WEEK_CHOICES, default=DAYS_OF_WEEK_CHOICES[0],
                                   verbose_name='День недели')
    tutor = models.ForeignKey(Tutor, on_delete=models.SET_DEFAULT, default=None, null=True)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        unique_together = ('time', 'location', 'day_of_week')

    def __str__(self):
        return f'{self.get_day_of_week_display()} {self.get_location_display()} {self.get_time_display()}'

    def get_students_amount(self):
        return self.students.count()


class Student(DeletedMixin):
    """
    Модель для хранения информации об ученике
    """
    objects = models.Manager()
    active = ActiveStudentsManager()

    name = models.CharField(max_length=50, blank=False, verbose_name='Фамилия Имя')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа',
                              related_name='students')
    kiberon_amount = models.PositiveIntegerField(default=0)
    info = models.TextField(max_length=250, blank=True, verbose_name='Информация')

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return self.name

    def add_kiberons(self, amount):
        self.kiberon_amount = F('kiberon_amount') + amount
        self.save()

    def delete_kiberons(self, amount):
        self.kiberon_amount = F('kiberon_amount') - amount
        self.save()


class Kiberon(models.Model):
    """
    Модель для хранения значению киберона по достижениям
    """
    ACHIEVEMENT_CHOICES = (
        ('visit', 'Посещение урока'),
        ('eyes', 'Разминка глаз'),
        ('fastest', 'Быстрее всех завершил задание'),
        ('homework', 'За выполнение домашнего задания'),
        ('instagram', 'За пост в instagram'),
        ('social', 'За посты в соц. сети'),
        ('custom', 'Свое достижение')
    )
    achievement = models.CharField(max_length=10, choices=ACHIEVEMENT_CHOICES, default=ACHIEVEMENT_CHOICES[0],
                                   unique=True, verbose_name='Достижение')
    value = models.PositiveSmallIntegerField(default=5, blank=False, verbose_name='Количество киберонов')

    class Meta:
        verbose_name = 'Печать'
        verbose_name_plural = 'Печати'

    def __str__(self):
        return f'{self.get_achievement_display()} - {self.value}к'


class KiberonStudentReg(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Студент')
    kiberon = models.ForeignKey(Kiberon, on_delete=models.CASCADE, verbose_name='Достижение')
    date = models.DateField(verbose_name='Дата', default=timezone.now)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, verbose_name='Тьютор')
    custom_kiberons = models.PositiveSmallIntegerField(verbose_name='Свое количество киберонов', default=0)

    class Meta:
        verbose_name = 'Запись о печати'
        verbose_name_plural = 'Записи о печатях'
        ordering = ('-date',)

    def __str__(self):
        return f'{self.student.name} - {self.kiberon.get_achievement_display()} - {self.date}'

    def clean(self):
        if self.kiberon.achievement != 'custom':
            reg = KiberonStudentReg.objects.filter(student=self.student, kiberon=self.kiberon, date=self.date)
            if reg.count() > 0:
                raise ValidationError(f'Запись с достижением "{self.kiberon.get_achievement_display()}"' \
                                      f' для {self.student.name} на {self.date} уже есть')
        else:
            super().clean()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.kiberon.achievement == 'custom':
            self.student.add_kiberons(self.custom_kiberons)
        else:
            self.student.add_kiberons(self.kiberon.value)
        super().save()

    def delete(self, using=None, keep_parents=False):
        if self.kiberon.achievement == 'custom':
            self.student.delete_kiberons(self.custom_kiberons)
        else:
            self.student.delete_kiberons(self.kiberon.value)
        super().delete()
