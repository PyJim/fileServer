from django.test import TestCase, Client
from django.urls import reverse
from .models import User


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.activate_user_url = reverse('activate_user', args=['uidb64', 'token'])
        self.request_activation_email_url = reverse('request_activation_email')
        self.reset_password_url = reverse('reset_password')
        self.forgot_password_url = reverse('forgot_password')
        self.reset_forgotten_password_url = reverse('reset_forgotten_password', args=['uidb64', 'token'])
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')

    def test_signup_view(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authenticate/signup.html')

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authenticate/login.html')

    def test_logout_view(self):
        self.client.force_login(self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)


    def test_activate_user_view(self):
        response = self.client.get(self.activate_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authenticate/activation_failed.html')

    def test_request_activation_email_view(self):
        response = self.client.get(self.request_activation_email_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authenticate/activation_failed.html')

    def test_reset_password_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.reset_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authenticate/reset_password.html')

    def test_forgot_password_view(self):
        response = self.client.get(self.forgot_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authenticate/forgot_password.html')

    def test_reset_forgotten_password_view(self):
        response = self.client.get(self.reset_forgotten_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authenticate/forgot_password_reset_failed.html')
