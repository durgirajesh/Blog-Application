from django.contrib import admin
from .models import PostModel

class PostModelAdmin(admin.ModelAdmin):
    list_display = ('postID', 'author', 'title', 'content', 'createdAtTime', 'createdAtDate', 'updatedAtTime', 'updatedAtDate')

admin.site.register(PostModel, PostModelAdmin)
