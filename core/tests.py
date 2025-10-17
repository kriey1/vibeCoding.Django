from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment, FileUpload
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile


class PostModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='tester', password='pass')
		self.post = Post.objects.create(author=self.user, title='테스트', content='내용')

	def test_post_str(self):
		self.assertEqual(str(self.post), '테스트')


class CommentModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='tester', password='pass')
		self.post = Post.objects.create(author=self.user, title='테스트', content='내용')
		self.comment = Comment.objects.create(post=self.post, author=self.user, content='댓글')

	def test_comment_str(self):
		self.assertEqual(str(self.comment), 'tester - 테스트')


class FileUploadModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='tester', password='pass')
		self.post = Post.objects.create(author=self.user, title='테스트', content='내용')
		self.file_upload = FileUpload.objects.create(
			post=self.post,
			uploader=self.user,
			file='test.txt',
			filename='test.txt'
		)

	def test_file_upload_str(self):
		self.assertEqual(str(self.file_upload), 'test.txt')


class PostAPITest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='apiuser', password='pass')
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)
		self.post = Post.objects.create(author=self.user, title='API테스트', content='API내용')

	def test_list_posts(self):
		response = self.client.get('/api/posts/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data[0]['title'], 'API테스트')

	def test_create_post(self):
		data = {'title': '새글', 'content': '새내용'}
		response = self.client.post('/api/posts/', data)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['title'], '새글')


class CommentAPITest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='commentuser', password='pass')
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)
		self.post = Post.objects.create(author=self.user, title='테스트', content='내용')
		self.comment = Comment.objects.create(post=self.post, author=self.user, content='댓글')

	def test_list_comments(self):
		response = self.client.get('/api/comments/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 1)

	def test_create_comment(self):
		data = {'post': self.post.id, 'content': '새 댓글'}
		response = self.client.post('/api/comments/', data)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['content'], '새 댓글')


class AuthenticationTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='authuser', email='test@example.com', password='testpass123')

	def test_signup_page(self):
		response = self.client.get(reverse('signup'))
		self.assertEqual(response.status_code, 200)

	def test_signup_post(self):
		data = {
			'username': 'newuser',
			'email': 'newuser@example.com',
			'password1': 'testpass123!',
			'password2': 'testpass123!'
		}
		response = self.client.post(reverse('signup'), data)
		self.assertEqual(response.status_code, 302)
		self.assertTrue(User.objects.filter(username='newuser').exists())

	def test_login_page(self):
		response = self.client.get(reverse('login'))
		self.assertEqual(response.status_code, 200)

	def test_logout(self):
		self.client.login(username='authuser', password='testpass123')
		response = self.client.get(reverse('logout'))
		self.assertEqual(response.status_code, 302)
