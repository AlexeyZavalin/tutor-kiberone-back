# Generated by Django 3.2.3 on 2021-12-14 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_siteconfiguration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='visited_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Последняя дата посещения'),
        ),
    ]
