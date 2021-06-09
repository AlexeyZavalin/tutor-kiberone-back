import random

from django.test import TestCase
from mainapp.models import Group, Student, Tutor


class TestGroup(TestCase):
    """ Тесты групп """
    def setUp(self) -> None:
        self.tutor = Tutor.objects.create(is_tutor=True, email='test@test.test', username='tutor', password='test')
        time = random.choice(Group.TIMES_CHOICES)
        location = random.choice(Group.LOCATION_CHOICES)
        day_of_week = random.choice(Group.DAYS_OF_WEEK_CHOICES)
        self.group = Group.objects.create(time=time, location=location, day_of_week=day_of_week, tutor=self.tutor)

    def test_group_students_amount(self):
        """  тестируем количество студентов в группе """
        self.assertEqual(self.group.get_students_amount(), 0)
        Student.objects.create(name='student', group=self.group)
        self.assertEqual(self.group.get_students_amount(), 1)
