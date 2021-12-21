# Generated by Django 3.2.3 on 2021-09-19 08:56

from django.db import migrations, IntegrityError


def create_kiberons(apps, schema_editor):
    """Создаем все виды киберонов"""
    Kiberon = apps.get_model('mainapp', 'Kiberon')
    try:
        Kiberon.objects.create(achievement=Kiberon.VISIT, value=10)
    except IntegrityError:
        pass
    try:
        Kiberon.objects.create(achievement=Kiberon.EYES, value=10)
    except IntegrityError:
        pass
    try:
        Kiberon.objects.create(achievement=Kiberon.FASTEST, value=5)
    except IntegrityError:
        pass
    try:
        Kiberon.objects.create(achievement=Kiberon.HOMEWORK, value=15)
    except IntegrityError:
        pass
    try:
        Kiberon.objects.create(achievement=Kiberon.INSTAGRAM, value=15)
    except IntegrityError:
        pass
    try:
        Kiberon.objects.create(achievement=Kiberon.SOCIAL, value=15)
    except IntegrityError:
        pass
    try:
        Kiberon.objects.create(achievement=Kiberon.ANSWER, value=5)
    except IntegrityError:
        pass
    try:
        Kiberon.objects.create(achievement=Kiberon.PERFECT_BEHAVIOUR_IN_MODULE, value=10)
    except IntegrityError:
        pass
    try:
        Kiberon.objects.create(achievement=Kiberon.HELP_TO_FRIEND, value=5)
    except IntegrityError:
        pass
    try:
        Kiberon.objects.create(achievement=Kiberon.VHELP_TO_ASSISTENTISIT, value=5)
    except IntegrityError:
        pass
    try:
        Kiberon.objects.create(achievement=Kiberon.USEFUL_RULE, value=10)
    except IntegrityError:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20210917_2112'),
    ]

    operations = [
        # migrations.RunPython(create_kiberons)
    ]
