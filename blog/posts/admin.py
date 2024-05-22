from django.contrib import admin
from .models import PostModel, CommentModel, ReplyModel

class PostModelAdmin(admin.ModelAdmin):
    list_display = ('postID', 'author', 'title', 'content', 'createdAtTime', 'createdAtDate', 'updatedAtTime', 'updatedAtDate')

class CommentsModelAdmin(admin.ModelAdmin):
    list_display = ('post', 'comment', 'commenter', 'RID')

class ReplyModelAdmin(admin.ModelAdmin):
    list_display = ('rid', 'username', 'reply')
    
admin.site.register(PostModel, PostModelAdmin)
admin.site.register(CommentModel, CommentsModelAdmin)
admin.site.register(ReplyModel, ReplyModelAdmin)