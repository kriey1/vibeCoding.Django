from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .serializers import PostSerializer
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

def post_list(request):
	posts = Post.objects.all().order_by('-created_at')
	return render(request, 'core/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'core/post_detail.html', {'post': post})

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

# Create your views here.
