# Generated by Django 3.2.3 on 2021-09-01 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='kiberon_amount',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество киберонов'),
        ),
    ]
