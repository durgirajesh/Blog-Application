from django.db import models
from users.models import UserModel

class PostModel(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.TextField(max_length=10, primary_key=True)
    content = models.TextField(max_length=1000)
    createdAtTime = models.TimeField(auto_now_add=True)
    createdAtDate = models.DateField(auto_now_add=True)
    updatedAtTime = models.TimeField(auto_now=True)
    updatedAtDate = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.title

class CommentsModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)

    def __str__(self) -> str:
        return self.comment