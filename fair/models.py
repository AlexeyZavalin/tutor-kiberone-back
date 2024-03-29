from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import F, Sum

from mainapp.mixins import DeletedMixin


class Souvenir(DeletedMixin):
    """ Модель сувенира ярмарки """
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Имя сувенира')
    image = models.ImageField(
        null=True,
        blank=True,
        verbose_name='Фото сувенира',
        upload_to='fair_souvenirs'
    )
    price = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(3500)],
        verbose_name='Стоимость в киберонах',
        null=False,
        blank=False,
        max_digits=4,
        decimal_places=0
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=0,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Сувенир'
        verbose_name_plural = 'Сувениры'
        ordering = ('price', 'amount')

    def __str__(self):
        return f'{self.name} - {self.price}K'

    def subtract_amount(self, amount: int) -> None:
        """
        Отнимаем количество
        amount: количество, которое нужно отнять
        """
        self.amount = F('amount') - amount
        self.save()


class FairRegistration(models.Model):
    """ Модель записи с сувенирами для студента """
    student = models.ForeignKey(
        'mainapp.Student',
        verbose_name='Ученик',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='students'
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата'
    )

    class Meta:
        verbose_name = 'Запись о ярмарке для ученика'
        verbose_name_plural = 'Записи о ярмарке для учеников'

    def __str__(self):
        return f'{self.student.name} - {self.date}'

    @property
    def total(self):
        """ получаем сумму в киберонах """
        return self.souvenirs.aggregate(Sum('price')).get('price__sum')


class FairRegistrationSouvenir(models.Model):
    """ Сувенир в записи ярмарки для ученика """
    souvenir = models.ForeignKey(
        Souvenir,
        verbose_name='Сувенир',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    price = models.DecimalField(
        verbose_name='Стоимость в киберонах в день ярмарки',
        null=False,
        blank=False,
        max_digits=4,
        decimal_places=0,
        default=Decimal(0)
    )
    fair_registration = models.ForeignKey(
        FairRegistration,
        on_delete=models.CASCADE,
        verbose_name='Запись о ярмарке',
        related_name='souvenirs'
    )

    class Meta:
        verbose_name = 'Сувенир в записи о ярмарке'
        verbose_name_plural = 'Сувениры в запясях о ярмарках'

    def __str__(self):
        return self.souvenir.__str__()

    def save(self, **kwargs: dict) -> None:
        self.souvenir.subtract_amount(1)
        super().save(**kwargs)
        
        
class Refund(models.Model):
    reason = models.TextField(
        verbose_name='Причина возврата',
        blank=True
    )
    fair_registration = models.OneToOneField(
        to=FairRegistration,
        verbose_name='Запись о ярмарке',
        on_delete=models.CASCADE
    )
    complete = models.BooleanField(
        verbose_name='Возврат завершен',
        default=False,
        editable=False
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата возврата'
    )

    class Meta:
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возвраты'

    def __str__(self):
        return self.fair_registration.__str__()

    def save(self, *args, **kwargs):
        if not self.complete:
            with transaction.atomic():
                self.fair_registration.student.add_kiberons(
                    self.fair_registration.total
                )
                self.complete = True
                # возвращаем количество
                for souvenir in self.fair_registration.souvenirs.all():
                    souvenir.souvenir.amount = F('amount') + 1
                    souvenir.souvenir.save()

        super().save(*args, **kwargs)
