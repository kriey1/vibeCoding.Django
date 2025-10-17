from django.contrib import admin
from .models import Post, UserProfile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "author", "created_at", "updated_at")
	search_fields = ("title", "content", "author__username")

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "created_at")
	search_fields = ("user__username",)
