# Generated by Django 3.2.6 on 2022-12-11 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_auto_20221211_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='slug',
            field=models.SlugField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='code',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='token',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
    ]
