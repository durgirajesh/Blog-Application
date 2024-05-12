from django.contrib import admin
from .models import PostModel, CommentsModel

class PostModelAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'content', 'createdAtTime', 'createdAtDate', 'updatedAtTime', 'updatedAtDate')

class CommentsModelAdmin(admin.ModelAdmin):
    list_display = ('post', 'comment')

admin.site.register(PostModel, PostModelAdmin)
admin.site.register(CommentsModel, CommentsModelAdmin)