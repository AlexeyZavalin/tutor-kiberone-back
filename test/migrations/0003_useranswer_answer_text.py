# Generated by Django 3.2.6 on 2023-01-27 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0002_auto_20230116_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='answer_text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст ответа'),
        ),
    ]
