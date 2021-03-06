# Generated by Django 3.2.3 on 2021-09-22 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0003_auto_20210919_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='temporary_tutor',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='temp_tutor', to=settings.AUTH_USER_MODEL, verbose_name='Временный тьютор'),
        ),
        migrations.AlterField(
            model_name='group',
            name='tutor',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='tutor', to=settings.AUTH_USER_MODEL, verbose_name='Тьютор'),
        ),
    ]
