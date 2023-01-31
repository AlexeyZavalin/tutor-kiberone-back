import json
import random

from django.test import TestCase, Client
from django.urls import reverse_lazy

from mainapp.models import Group, Student, AvailableTime, Location

from authapp.models import Tutor


class TestGroup(TestCase):
    """ Тесты групп """
    def setUp(self) -> None:
        self.tutor = Tutor.objects.create(
            is_tutor=True,
            email='test@test.test',
            username='tutor',
            password='test'
        )
        self.time = AvailableTime.objects.create(
            time_start='12:00',
            time_end='14:00'
        )
        self.location = Location.objects.create(
            address='test',
            short_name='test'
        )
        day_of_week = random.choice(Group.DAYS_OF_WEEK_CHOICES)
        self.group = Group.objects.create(
            available_time=self.time,
            available_location=self.location,
            day_of_week=day_of_week[0],
            tutor=self.tutor
        )
        self.client = Client()

    def test_group_students_amount(self):
        """  тестируем количество студентов в группе """
        self.assertEqual(self.group.students_amount, 0)
        Student.objects.create(name='student', group=self.group)
        self.assertEqual(self.group.students_amount, 1)

        # создаем скрытого студента
        Student.objects.create(
            name='student',
            group=self.group,
            is_deleted=True
        )
        self.assertEqual(self.group.students_amount, 1)

    def test_groups_unauth(self):
        """
        тестируем переход в группу неавторизованным пользователем
        """
        url = reverse_lazy('mainapp:groups')
        response = self.client.get(url)
        self.assertRedirects(
            response,
            f'{reverse_lazy("authapp:login")}?next={url}'
        )

    def test_groups_auth(self):
        """
        тестируем переход в группу авторизованным пользователем
        """
        url = reverse_lazy('mainapp:groups')
        self.client.force_login(self.tutor)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 201)

    def test_group_unauth(self):
        url = reverse_lazy(
            'mainapp:student-list',
            kwargs={
                'group_id': self.group.pk
            }
        )
        response = self.client.get(url)
        self.assertRedirects(
            response,
            f'{reverse_lazy("authapp:login")}?next={url}'
        )

    def test_group_auth(self):
        url = reverse_lazy(
            'mainapp:student-list',
            kwargs={
                'group_id': self.group.pk
            }
        )
        self.client.force_login(self.tutor)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_group_unauth(self):
        data = {}
        url = reverse_lazy('mainapp:create-group')
        response = self.client.post(url, data)
        self.assertRedirects(
            response,
            f'{reverse_lazy("authapp:login")}?next={url}'
        )

    def test_create_group_auth(self):
        data = {
            'location': self.location.pk,
            'time': self.time.pk,
            'day_of_week': random.choice(Group.DAYS_OF_WEEK_CHOICES)[0]
        }
        url = reverse_lazy('mainapp:create-group')
        url_groups = reverse_lazy('mainapp:groups')
        self.client.force_login(self.tutor)
        response = self.client.post(
            url,
            json.dumps(data),
            content_type='application/json'
        )
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_content.get('success'))
        self.assertEqual(response_content.get('redirect'), url_groups)

        # создание такой же группы
        response = self.client.post(
            url,
            json.dumps(data),
            content_type='application/json'
        )
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response_content.get('success'))
        self.assertEqual(
            response_content.get('message'),
            'Такая группа уже есть, измените параметры'
        )

    def test_remove_group(self):
        data = {
            'group_id': self.group.pk,
            'password': 'test'
        }
        url = reverse_lazy('mainapp:remove-group')
        url_groups = reverse_lazy('mainapp:groups')
        self.client.force_login(self.tutor)
        response = self.client.post(
            url,
            json.dumps(data),
            content_type='application/json'
        )
        response_content = json.loads(response.content)
        self.assertFalse(response_content.get('success'))
        self.assertEqual(
            response_content.get('message'),
            'Неверный пароль'
        )
