from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api/posts', views.PostViewSet)
router.register(r'api/comments', views.CommentViewSet)
router.register(r'api/files', views.FileUploadViewSet)

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_update, name='post_update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/comment/', views.comment_create, name='comment_create'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('post/<int:pk>/upload/', views.file_upload, name='file_upload'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='django_login'),
    path('', include(router.urls)),
]
