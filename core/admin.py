from django.contrib import admin
from .models import Post, UserProfile, Comment, FileUpload


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "author", "created_at", "updated_at")
	list_filter = ("created_at", "updated_at", "author")
	search_fields = ("title", "content", "author__username")
	date_hierarchy = "created_at"
	readonly_fields = ("created_at", "updated_at")
	fieldsets = (
		("기본 정보", {
			"fields": ("author", "title", "content")
		}),
		("날짜 정보", {
			"fields": ("created_at", "updated_at")
		}),
	)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "created_at")
	search_fields = ("user__username", "bio")
	readonly_fields = ("created_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ("id", "post", "author", "content_preview", "created_at", "updated_at")
	list_filter = ("created_at", "updated_at", "author")
	search_fields = ("content", "author__username", "post__title")
	date_hierarchy = "created_at"
	readonly_fields = ("created_at", "updated_at")
	
	def content_preview(self, obj):
		return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
	content_preview.short_description = "내용 미리보기"


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
	list_display = ("id", "filename", "post", "uploader", "created_at")
	list_filter = ("created_at", "uploader")
	search_fields = ("filename", "uploader__username", "post__title")
	date_hierarchy = "created_at"
	readonly_fields = ("created_at", "filename")
	fieldsets = (
		("파일 정보", {
			"fields": ("file", "filename", "post", "uploader")
		}),
		("날짜 정보", {
			"fields": ("created_at",)
		}),
	)
