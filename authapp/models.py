from django.db import models
from django.contrib.auth.models import AbstractUser


class Tutor(AbstractUser):
    is_tutor = models.BooleanField(verbose_name='Статус тьютора',
                                   default=False)
    email = models.EmailField(verbose_name='email address', blank=False,
                              unique=True)
    dark_theme_enabled = models.BooleanField(
        verbose_name='Темная тема включена',
        default=False
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Тьютор'
        verbose_name_plural = 'Тьюторы'

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
