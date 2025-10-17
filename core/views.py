from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Post, Comment, FileUpload
from .serializers import PostSerializer, CommentSerializer, FileUploadSerializer
from .forms import SignUpForm
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all().order_by('-created_at')
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all().order_by('-created_at')
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)


class FileUploadViewSet(viewsets.ModelViewSet):
	queryset = FileUpload.objects.all().order_by('-created_at')
	serializer_class = FileUploadSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def perform_create(self, serializer):
		file = self.request.FILES.get('file')
		filename = file.name if file else 'unknown'
		serializer.save(uploader=self.request.user, filename=filename)

def post_list(request):
	posts = Post.objects.all().order_by('-created_at')
	return render(request, 'core/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	comments = post.comments.all().order_by('-created_at')
	return render(request, 'core/post_detail.html', {'post': post, 'comments': comments})

@login_required
def post_create(request):
	if request.method == 'POST':
		title = request.POST.get('title')
		content = request.POST.get('content')
		post = Post.objects.create(author=request.user, title=title, content=content)
		return redirect('post_detail', pk=post.pk)
	return render(request, 'core/post_form.html')

@login_required
def post_update(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.user != post.author:
		return HttpResponse('권한이 없습니다.', status=403)
	if request.method == 'POST':
		post.title = request.POST.get('title')
		post.content = request.POST.get('content')
		post.save()
		return redirect('post_detail', pk=post.pk)
	return render(request, 'core/post_form.html', {'post': post})

@login_required
def post_delete(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.user != post.author:
		return HttpResponse('권한이 없습니다.', status=403)
	if request.method == 'POST':
		post.delete()
		return redirect('post_list')
	return render(request, 'core/post_confirm_delete.html', {'post': post})


def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, '회원가입이 완료되었습니다.')
			return redirect('post_list')
	else:
		form = SignUpForm()
	return render(request, 'core/signup.html', {'form': form})


def user_login(request):
	return render(request, 'core/login.html')


def user_logout(request):
	logout(request)
	messages.success(request, '로그아웃되었습니다.')
	return redirect('post_list')


@login_required
def comment_create(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		content = request.POST.get('content')
		if content:
			Comment.objects.create(post=post, author=request.user, content=content)
			messages.success(request, '댓글이 작성되었습니다.')
		return redirect('post_detail', pk=pk)
	return redirect('post_detail', pk=pk)


@login_required
def comment_delete(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	post_pk = comment.post.pk
	if request.user != comment.author:
		return HttpResponse('권한이 없습니다.', status=403)
	if request.method == 'POST':
		comment.delete()
		messages.success(request, '댓글이 삭제되었습니다.')
		return redirect('post_detail', pk=post_pk)
	return redirect('post_detail', pk=post_pk)


@login_required
def file_upload(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST' and request.FILES.get('file'):
		file = request.FILES['file']
		FileUpload.objects.create(
			post=post,
			uploader=request.user,
			file=file,
			filename=file.name
		)
		messages.success(request, '파일이 업로드되었습니다.')
		return redirect('post_detail', pk=pk)
	return redirect('post_detail', pk=pk)
