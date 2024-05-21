import uuid
from django.db import models
from users.models import UserModel

class PostModel(models.Model):
    postID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.TextField(max_length=10)
    content = models.TextField(max_length=1000)
    createdAtTime = models.TimeField(auto_now_add=True)
    createdAtDate = models.DateField(auto_now_add=True)
    updatedAtTime = models.TimeField(auto_now=True)
    updatedAtDate = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class ReplyModel(models.Model):
    rid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reply = models.TextField(max_length=15)
    username = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.reply

class CommentModel(models.Model):
    commentId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField(max_length=20)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    commenter = models.ForeignKey(UserModel, null=True, on_delete=models.SET_NULL)
    RID = models.ForeignKey(ReplyModel, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.comment