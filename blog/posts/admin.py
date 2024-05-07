from django.contrib import admin
from .models import post_model

class PostModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'createdAtTime', 'createdAtDate', 'updatedAtTime', 'updatedAtDate')

admin.site.register(post_model, PostModelAdmin)
