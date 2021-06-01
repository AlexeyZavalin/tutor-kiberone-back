# Generated by Django 3.2.3 on 2021-05-31 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kiberonstudentreg',
            name='custom_kiberons',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Свое количество киберонов'),
        ),
        migrations.AlterField(
            model_name='kiberon',
            name='achievement',
            field=models.CharField(choices=[('visit', 'Посещение урока'), ('eyes', 'Разминка глаз'), ('fastest', 'Быстрее всех завершил задание'), ('homework', 'За выполнение домашнего задания'), ('instagram', 'За пост в instagram'), ('social', 'За посты в соц. сети'), ('custom', 'Свое достижение')], default=('visit', 'Посещение урока'), max_length=10, unique=True, verbose_name='Достижение'),
        ),
    ]
