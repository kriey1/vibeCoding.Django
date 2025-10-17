from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post
from rest_framework.test import APIClient

class PostModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='tester', password='pass')
		self.post = Post.objects.create(author=self.user, title='테스트', content='내용')

	def test_post_str(self):
		self.assertEqual(str(self.post), '테스트')

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
