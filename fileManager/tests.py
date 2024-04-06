from django.test import TestCase, Client
from django.urls import reverse
from .models import File
from userAuth.models import User
from userAuth.backends import EmailBackend  # Import the custom authentication backend


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.feed_url = reverse('feed')
        self.file = File.objects.create(title='Test File', description='Test Description', file='test.txt')
        self.user = User.objects.create_user(email='test@example.com', password='password')

        # Authenticate user using EmailBackend and force login
        self.authenticated_user = EmailBackend().authenticate(username='test@example.com', password='password')
        self.client.force_login(self.authenticated_user)

    def test_files_page_GET_authenticated(self):
        response = self.client.get(self.feed_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files.html')

    def test_files_page_GET_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.feed_url)
        # Redirect to login page when not authenticated
        self.assertRedirects(response, reverse('login') + '?next=' + self.feed_url)

    def test_files_page_POST_authenticated(self):
        response = self.client.post(self.feed_url, {'query': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files.html')

    def test_files_page_POST_unauthenticated(self):
        self.client.logout()
        response = self.client.post(self.feed_url, {'query': 'Test'})
        # Redirect to login page when not authenticated
        self.assertRedirects(response, reverse('login') + '?next=' + self.feed_url)

    def test_email_file_GET_authenticated(self):
        response = self.client.get(reverse('email_file', args=[self.file.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'send_file.html')

    def test_email_file_GET_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('email_file', args=[self.file.id]))
        # Redirect to login page when not authenticated
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('email_file', args=[self.file.id]))

    def test_email_file_POST_authenticated(self):
        response = self.client.post(reverse('email_file', args=[self.file.id]), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('feed'))

    def test_email_file_POST_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse('email_file', args=[self.file.id]), {'email': 'test@example.com'})
        # Redirect to login page when not authenticated
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('email_file', args=[self.file.id]))

    def test_download_file(self):
        response = self.client.get(reverse('download_file', args=[self.file.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/force-download')
        self.assertEqual(response['Content-Disposition'], f'attachment; filename=test.txt')
