from django.contrib import admin
from .models import PostModel

class PostModelAdmin(admin.ModelAdmin):
    list_display = ('postID', 'author', 'title', 'content', 'createdAtTime', 'createdAtDate', 'updatedAtTime', 'updatedAtDate')

class CommentsModelAdmin(admin.ModelAdmin):
    list_display = ('post', 'comment')

admin.site.register(PostModel, PostModelAdmin)
# admin.site.register(CommentsModel, CommentsModelAdmin)