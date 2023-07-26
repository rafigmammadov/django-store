from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.models import User


class RegisterCreateTestView(TestCase):


    def user_creation(self):
        self.path_creation = reverse('users:register')
        self.data_creation =  {'first_name': 'test', 'last_name': 'test', 'username': 'rafig', 'email': 'rafig@mail.ru',
                'password1': 'Password12P', 'password2': 'Password12P'}
        self.response_creation = self.client.post(self.path_creation, self.data_creation)

        return self.path_creation, self.data_creation, self.response_creation

    def setUp(self):
        pass

    def test_register_get_method(self):
        path = reverse('users:register')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_post_method(self):
        path_creation, data_creation, response_creation = self.user_creation()

        user = User.objects.get(username='rafig')
        self.assertEqual(user.username, 'rafig')

        self.assertTrue(User.objects.filter(username='rafig').exists())
        self.assertEqual(response_creation.status_code, HTTPStatus.FOUND)

    def test_login_post_method(self):
        path_creation, data_creation, response_creation = self.user_creation()

        self.assertTrue(User.objects.filter(username='rafig').exists())

        path = reverse('users:login')
        data={'username': 'rafig', 'password': 'Password12P'}
        response = self.client.post(path, data)

        user = User.objects.filter(username='rafig')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)