from django.test import TestCase, Client
from django.urls import reverse
from fileManager.models import File
from userAuth.models import User
from userAuth.backends import EmailBackend


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.files_url = reverse('files')
        self.upload_url = reverse('upload')
        self.user = User.objects.create_user(email='test@example.com', password='password', is_staff=True)

        # Authenticate staff user using EmailBackend and force login
        self.authenticated_user = EmailBackend().authenticate(username='test@example.com', password='password')
        self.client.force_login(self.authenticated_user)

    def test_files_page_GET_authenticated(self):
        response = self.client.get(self.files_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/files.html')

    def test_files_page_GET_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.files_url)
        # Redirect to login page when not authenticated
        self.assertRedirects(response, reverse('login') + '?next=' + self.files_url)

    def test_upload_file_GET_authenticated(self):
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/fileupload.html')

    def test_upload_file_GET_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.upload_url)
        # Redirect to login page when not authenticated
        self.assertRedirects(response, reverse('login') + '?next=' + self.upload_url)

    def test_upload_file_POST_authenticated(self):
        response = self.client.post(self.upload_url, {'title': 'Test', 'description': 'Test Description', 'file': 'testfile.txt'})
        self.assertRedirects(response, reverse('files'))

    def test_upload_file_POST_unauthenticated(self):
        self.client.logout()
        response = self.client.post(self.upload_url, {'title': 'Test', 'description': 'Test Description', 'file': 'testfile.txt'})
        # Redirect to login page when not authenticated
        self.assertRedirects(response, reverse('login') + '?next=' + self.upload_url)

