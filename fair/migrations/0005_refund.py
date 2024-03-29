# Generated by Django 3.2.6 on 2022-12-25 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fair', '0004_alter_fairregistrationsouvenir_fair_registration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(blank=True, verbose_name='Причина возврата')),
                ('complete', models.BooleanField(default=False, verbose_name='Возврат завершен')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата возврата')),
                ('fair_registration', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='fair.fairregistration', verbose_name='Запись о ярмарке')),
            ],
        ),
    ]
